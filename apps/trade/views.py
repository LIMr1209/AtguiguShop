import os
from datetime import datetime

from django.shortcuts import render, redirect
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from AtguiguShop.settings import app_private_key_path, alipay_public_key_path
from utils.alipay import AliPay
from utils.permission import IsOwnerOrReadOnly
from .models import ShopingCart, OrderInfo, OrderGoods
from .serializers import ShopingCartSerializer, ShopingDetailCartSerializer, OrderInfoSerializer, \
    OrderInfoDetailSerializer
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.views import APIView
from rest_framework.response import Response


# Create your views here.

# 购物车
class ShopingCartViewSet(ModelViewSet):
    '''
    create:
        加入购物车
    list:
        得到购物车商品列表
    destroy:
        删除购物车商品
    update:
        更新购物车商品信息
    '''

    # serializer_class = ShopingCartSerializer
    permission_classes = (IsOwnerOrReadOnly, IsAuthenticated)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    lookup_field = 'goods_id'

    def get_queryset(self):
        return ShopingCart.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'list':
            return ShopingDetailCartSerializer
        else:
            return ShopingCartSerializer

    # 实现当添加商品到购物车时，库存减少
    def perform_create(self, serializer):
        shop_cat = serializer.save()
        goods = shop_cat.goods
        goods.goods_num -= shop_cat.nums
        goods.save()

    # 实现当从购物车删除商品时，库存增加
    def perform_destroy(self, instance):
        goods = instance.goods
        goods.goods_num += instance.nums
        goods.save()
        # instance.delete 是原来的
        instance.delete()

    # 实现修改购物车商品数量，库存改变
    def perform_update(self, serializer):
        # 原来的serializer.save()

        # 保存前的购物车对象
        old_shop_cart = ShopingCart.objects.filter(id=serializer.instance.id)[0]
        # 保存前的数量
        old_nums = old_shop_cart.nums
        # 保存后的购物车对象
        new_shop_cart = serializer.save()
        new_nums = new_shop_cart.nums
        # 差值
        nums = new_nums-old_nums
        print(nums)
        # 得到购物车商品
        goods = old_shop_cart.goods
        goods.goods_num -= nums
        goods.save()


# 订单不允许修改的
class OrderInfoViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.RetrieveModelMixin,
                       mixins.DestroyModelMixin, mixins.ListModelMixin):
    '''
    create:
        创建订单
    list:
        所有订单信息
    destroy:
        删除订单
    '''
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return OrderInfoDetailSerializer
        else:
            return OrderInfoSerializer

    def get_queryset(self):
        return OrderInfo.objects.filter(user=self.request.user)

    # 自定义提交订单 ,不需要返回值,订单提交后，清空购物车 把购物车的信息添加到OrderGoods中来
    def perform_create(self, serializer):
        order_info = serializer.save()  # 保存订单
        shop_carts = ShopingCart.objects.filter(user=self.request.user)
        for shop_cart in shop_carts:
            order_goods = OrderGoods()
            order_goods.order = order_info
            order_goods.goods = shop_cart.goods
            order_goods.good_nums = shop_cart.nums
            order_goods.save()
            shop_cart.delete()  # 删除购物车


class AliPayView(APIView):
    # 如果用网页登陆支付，走这里
    def get(self, request):
        processed_dict = {}
        for key, value in request.GET.items():
            processed_dict[key] = value
        # 得到签名
        sign = processed_dict.pop("sign", None)

        alipay = AliPay(

            appid=os.environ.get('APPID'),  # APPID
            # 异步通知，回调这个路径，通知自己的服务器
            app_notify_url="http://127.0.0.1:8000/alipay/return",
            app_private_key_path=app_private_key_path,  # 应用私钥
            alipay_public_key_path=alipay_public_key_path,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            debug=True,  # 默认False,
            # 同步通知,通知自己的服务器
            return_url="http://127.0.0.1:8000/alipay/return"
        )
        # 验证 签名
        verify_result = alipay.verify(processed_dict, sign)
        print(verify_result)

        if verify_result:
            # 交易号
            trade_no = processed_dict.get("trade_no")
            # 订单号
            order_sn = processed_dict.get("out_trade_no")
            # 支付状态
            pay_status = processed_dict.get("pay_status", "TRADE_SUCCESS")
            # 查询是否有订单
            orders = OrderInfo.objects.filter(order_sn=order_sn)

            for order in orders:
                # 具体订单的交易号
                order.trade_no = trade_no

                # 修改订单的状态,成功
                order.pay_status = pay_status

                # 支付成功的时间
                order.pay_time = datetime.now()

                # 保存状态
                order.save()
            response = redirect('index')
            response.set_cookie('nextPath', 'pay', max_age=2)
            return response

    # 如果用沙箱客户端扫描支付走这里
    def post(self, request):
        processed_dict = {}
        for key, value in request.POST.items():
            processed_dict[key] = value
        sign = processed_dict.pop('sign', None)
        alipay = AliPay(

            appid=os.environ.get('APPID'),  # APPID
            # 异步通知，回调这个路径，通知自己的服务器
            app_notify_url="http://127.0.0.1:8000/alipay/return",
            app_private_key_path=app_private_key_path,  # 应用私钥
            alipay_public_key_path=alipay_public_key_path,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            debug=True,  # 默认False,
            # 同步通知,通知自己的服务器
            return_url="http://127.0.0.1:8000/alipay/return"
        )
        # 验证 签名
        verify_result = alipay.verify(processed_dict, sign)
        if verify_result:
            trade_no = processed_dict.get("trade_no")
            # 订单号
            order_sn = processed_dict.get("out_trade_no")
            # 支付状态
            pay_status = processed_dict.get("pay_status", "TRADE_SUCCESS")
            # 查询是否有订单
            orders = OrderInfo.objects.filter(order_sn=order_sn)

            for order in orders:
                # 具体订单的交易号
                order.trade_no = trade_no

                # 修改订单的状态,成功
                order.pay_status = pay_status

                # 支付成功的时间
                order.pay_time = datetime.now()

                # 保存状态
                order.save()
            response = redirect('index')
            response.set_cookie('nextPath', 'pay', max_age=2)
            return response
