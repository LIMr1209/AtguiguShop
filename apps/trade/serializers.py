from rest_framework import serializers
from goods.models import Goods
from .models import ShopingCart, OrderInfo, OrderGoods
from goods.serializers import GoodsSerializer
from AtguiguShop.settings import alipay_public_key_path, app_private_key_path
from utils.alipay import AliPay
import os

# 购物车序列化器
class ShopingCartSerializer(serializers.Serializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    nums = serializers.IntegerField(required=True, min_value=1, error_messages={
        'required': '请选择购买数量',
        'min_value': '最小数量为1'
    }, help_text='商品数量', label='商品数量')
    goods = serializers.PrimaryKeyRelatedField(required=True, queryset=Goods.objects.all(), help_text='商品名',
                                               label='商品名')

    # validated_data 为请求的数据
    def create(self, validated_data):
        user = self.context['request'].user
        nums = validated_data['nums']
        goods = validated_data['goods']
        exised = ShopingCart.objects.filter(user=user, goods=goods)
        # 如果购物车存在该商品,加购数量
        if exised:
            exised = exised[0]
            exised.nums += nums
            exised.save()
        # 不存在,创建
        else:
            exised = ShopingCart.objects.create(**validated_data)
        # 必须返回
        return exised

    def update(self, instance, validated_data):
        # instance 购物车model实例化对象
        instance.nums = validated_data['nums']
        instance.save()
        # 必须返回
        return instance


# class ShopingCartSerializer1(serializers.ModelSerializer):
#     user = serializers.HiddenField(default=serializers.CurrentUserDefault())
#
#     nums = serializers.IntegerField(required=True, min_value=1, error_messages={
#         'required': '请选择购买数量',
#         'min_value': '最小数量为1'
#     }, help_text='加购数量',label='商品数量')
#     goods = serializers.PrimaryKeyRelatedField(required=True, queryset=Goods.objects.all(), help_text='商品名',label='商品名')
#
#     def create(self, validated_data):
#         user = self.context['request'].user
#         nums = validated_data['nums']
#         goods = validated_data['goods']
#         exised = ShopingCart.objects.filter(user=user, goods=goods)
#         if exised:
#             exised = exised[0]
#             exised.nums += nums
#             exised.save()
#         else:
#             exised = ShopingCart.objects.create(**validated_data)
#         return exised
#
#     def update(self, instance, validated_data):
#         instance.nums = validated_data['nums']
#         instance.save()
#         return instance
#
#     class Meta:
#         model = ShopingCart
#         fields = ('user','goods','nums')

class ShopingDetailCartSerializer(serializers.ModelSerializer):
    goods = GoodsSerializer()

    class Meta:
        model = ShopingCart
        fields = '__all__'


class OrderInfoSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    # 订单号不让前端编写
    order_sn = serializers.CharField(read_only=True)
    # 交易号不让前端编写
    trade_sn = serializers.CharField(read_only=True)
    # 支付状态
    pay_status = serializers.CharField(read_only=True)
    # 支付时间
    pay_time = serializers.DateTimeField(read_only=True,format='%Y-%m-%d %H:%M')
    # 添加时间
    add_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M')

    def generate_order_sn(self):
        import time
        import datetime
        from random import randint
        order_sn = '{}{}{}'.format(datetime.datetime.now().strftime('%Y%m%d%H%M%S'),
                                   self.context['request'].user.username,
                                   randint(11, 99))
        print(self.context['request'].user.username)
        return order_sn

    def validate(self, attrs):
        attrs['order_sn'] = self.generate_order_sn()
        return attrs

    class Meta:
        model = OrderInfo
        fields = '__all__'


class OrderGoodsSerializer(serializers.ModelSerializer):
    goods = GoodsSerializer(many=False)

    class Meta:
        model = OrderGoods
        fields = '__all__'


class OrderInfoDetailSerializer(serializers.ModelSerializer):
    goods = OrderGoodsSerializer(many=True)
    # 支付宝url
    alipay_url = serializers.SerializerMethodField(read_only=True)

    # instance就是OrderInfoDetailSerializer对象  get_字段() ,支付宝支付函数
    def get_alipay_url(self, instance):
        alipay = AliPay(
            appid=os.environ.get('APPID'),  # APPID
            # 异步通知，回调这个路径，通知自己的服务器
            app_notify_url="http://127.0.0.1:8000/alipay/return",
            app_private_key_path=app_private_key_path,  # 应用私钥
            alipay_public_key_path=alipay_public_key_path,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            debug=True,  # 默认False,
            # 同步通知,通知自己的服务器
            return_url="http://127.0.0.1:8000/alipay/return",
        )
        url = alipay.direct_pay(
            subject=instance.order_sn,
            # 商品id
            out_trade_no=instance.order_sn,
            # 资金
            total_amount=instance.order_mount
        )
        re_url = "https://openapi.alipaydev.com/gateway.do?{data}".format(data=url)
        return re_url

    class Meta:
        model = OrderInfo
        fields = '__all__'
