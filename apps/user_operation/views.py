from django.shortcuts import render
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from .models import UserFav, UserLeavingMessage, UserAddress
from .serializer import UserFavSerializer, UserFavDetailSerializer, LeavingMessageSerializers, UserAddressSerializers
from rest_framework.permissions import IsAuthenticated
from utils.permission import IsOwnerOrReadOnly
from rest_framework_jwt.authentication import JSONWebTokenAuthentication


# 用户收藏接口实现

class UserFavViewSet(viewsets.GenericViewSet, mixins.DestroyModelMixin, mixins.ListModelMixin, mixins.CreateModelMixin,
                     mixins.RetrieveModelMixin):
    '''
    destroy:
        取消收藏
    list:
        收藏列表
    retrieve:
        收藏详情
    create:
        收藏商品
    '''
    # 权限认证
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    # token 认证 有JSONWebTokenAuthentication，需要有SessionAuthentication(用户session)没有登陆不上
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    # 支持外键字段 实现 RetrieveModelMixin 获取详情信息时,/2/ 2指定的是商品id,本来是用户收藏表的id字段
    lookup_field = 'goods_id'

    # get_serializer_class 上面不需定义serializer_class
    def get_serializer_class(self):
        if self.action == 'create':
            # 创建收藏的序列化器
            return UserFavSerializer
        else:
            # 收藏列表,收藏详情,取消收藏的序列化器
            return UserFavDetailSerializer

    # 也可以 使用信号量实现 goods收藏数，收藏数+1
    def perform_create(self, serializer):
        # instance 为Userfav model 实例
        # 实现
        instance = serializer.save()
        goods = instance.goods
        goods.fav_num += 1
        goods.save()

    # 取消收藏 收藏数 -1
    def perform_destroy(self, instance):
        goods = instance.goods
        # 让收藏数加1
        goods.fav_num -= 1
        # 保存数据
        goods.save()
        instance.delete()

    # 重写 get_queryset ,list 返回请求用户的收藏数据
    def get_queryset(self):  # 有这个方法就不用写 queryset ,但是url中需指定base_name
        return UserFav.objects.filter(user=self.request.user)


# 用户留言

class LeavingMessageViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.ListModelMixin,
                            mixins.DestroyModelMixin):
    '''
    create:
        创建留言
    list:
        留言列表
    destroy:
        删除留言
    '''
    serializer_class = LeavingMessageSerializers
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    def get_queryset(self):
        return UserLeavingMessage.objects.filter(user=self.request.user)


#  ModelViewSet 集成CreateModelMixin,RetrieveModelMixin,UpdateModelMixin,DestroyModelMixin,ListModelMixin,GenericViewSet
class UserAddressViewSet(ModelViewSet):
    '''
    create:
        新建收货地址
    destroy:
        删除收货地址
    list:
        收货地址列表
    update:
        修改收货地址
    retrieve:
        单个详情收货地址
    '''
    serializer_class = UserAddressSerializers
    authentication_classes = (SessionAuthentication, JSONWebTokenAuthentication)
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)

    def get_queryset(self):
        return UserAddress.objects.filter(user=self.request.user)
