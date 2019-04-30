from django.shortcuts import render
from .models import Goods, GoodsCategory, Banner
from .serializers import GoodsSerializer, GoodsCategorySerializer1, BannerSerializer, IndexCategorySerializer
# from rest_framework.views import Response
# from rest_framework.response import Response
# from rest_framework.views import APIView
from rest_framework import mixins
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from .filters import GoodsFilter
from rest_framework import filters
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework_extensions.mixins import CacheResponseMixin
from rest_framework.throttling import UserRateThrottle,AnonRateThrottle


# 根据前端项目 创建自定义 分页器
# 配置后 settings 可以不配置分页功能
class Pagination(PageNumberPagination):
    # 默认返回10条
    page_size = 12
    # 每页返回多少条的参数变量
    page_size_query_param = 'page_size'
    page_query_param = 'page'  # p  页码的定义   url后 显示的参数key  ?p=1
    # 最大返回100条
    max_page_size = 100


# Create your views here.

# class GoodsListView(APIView):
#     def get(self, request, format=None):
#         goods_list = Goods.objects.all()[:10]
#         goods_serializer = GoodsSerializer(goods_list, many=True)
#         return Response(goods_serializer.data)

# 第一种
# class GoodsListView(mixins.ListModelMixin,generics.GenericAPIView):
#     queryset = Goods.objects.all()[:10]  #queryset 名词不能变
#     serializer_class = GoodsSerializer   # serializer_class 名词不能变
#     def get(self,request,*args,**kwargs):
#         return self.list(request,*args,**kwargs)
# ListAPIView  和    ListModelMixin  处理get 请求
# 第二种   #ListAPIView已经封装了get方法 和 GenericAPIView
# class GoodsListView(generics.ListAPIView):
#     queryset = Goods.objects.all()  # queryset 名词不能变
#     serializer_class = GoodsSerializer  # serializer_class 名词不能变
#     pagination_class = GoodsListPagination  # 配置分页(settings 有，则不需配置)

# CacheResponseMixin 缓存机制，要放在最前面
class GoodsListViewSet(CacheResponseMixin,mixins.ListModelMixin, viewsets.GenericViewSet, mixins.RetrieveModelMixin):
    '''
    list:
        得到商品列表
    retrieve:
        得到商品详情
    '''
    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer
    pagination_class = Pagination
    # 单独的token认证，不通过不返回数据
    authentication_classes = (TokenAuthentication,)
    # 局部访问限制 配置
    throttle_classes = (AnonRateThrottle,UserRateThrottle)

    # 重写retrieve方法 实现进入goods 详情 点击数+1
    # 原来的
    # def retrieve(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     serializer = self.get_serializer(instance)
    #     return Response(serializer.data)
    def retrieve(self, request, *args, **kwargs):
        # instance 为商品 model 实例
        instance = self.get_object()
        instance.click_num += 1
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

        # def get_queryset(self):

    #     # return Goods.objects.filter(shop_price__gte=100)
    #     queryset = Goods.objects.all()
    #     min_price = self.request.query_params.get('min_price',0)
    #     if min_price:
    #         queryset = Goods.objects.filter(shop_price__gt=int(min_price))
    #     return queryset
    # filter_backends = (DjangoFilterBackend,)
    # filter_fields = ('name','shop_price') # 过滤字段
    #   支持搜索和过滤,排序，写在一起
    filter_backends = (filters.OrderingFilter, filters.SearchFilter, DjangoFilterBackend)
    filter_class = GoodsFilter
    #
    search_fields = ('name', 'goods_brief', 'goods_desc')  # 搜索字段 不写就没有搜索框
    ordering_fields = ('shop_price', 'add_time', 'sold_num')  # 排序字段 # 不写的话排序所有字段
    # ordering_fields = '__all__'    #相当于不写
    # search_fields = ('^name', '=goods_brief', 'goods_desc')


# 商品类别                    # ListModeMixin   是get方法获取所有的类别            RetrieveModelMixin 是根据Id获取单个类别的类，categorys/1
class GoodCategoryListViewSet(mixins.ListModelMixin, viewsets.GenericViewSet, mixins.RetrieveModelMixin):
    '''
    list:
        商品类别列表
    retrieve:
        单个商品类别详情
    '''
    queryset = GoodsCategory.objects.filter(category_type=1)  # 一级类目
    # 不写分页器
    serializer_class = GoodsCategorySerializer1


# 首页轮播

class BannerViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    '''
    list:
        首页轮播图
    '''
    queryset = Banner.objects.all()
    serializer_class = BannerSerializer


class IndexCategoryViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = GoodsCategory.objects.filter(is_tab=True, name__in=['生鲜食品', '酒水饮料'])
    # 找到导航，且类别为生鲜食品和酒水饮料的商品类别
    serializer_class = IndexCategorySerializer
