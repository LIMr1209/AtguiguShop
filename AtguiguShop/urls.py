"""AtguiguShop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
import xadmin
from .settings import MEDIA_ROOT
from django.views.static import serve
from goods.views import GoodsListViewSet, GoodCategoryListViewSet, BannerViewSet, IndexCategoryViewSet
from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views
from rest_framework_jwt.views import obtain_jwt_token
from users.views import SmsCodeViewSet, UserViewSet
from user_operation.views import UserFavViewSet, LeavingMessageViewSet, UserAddressViewSet
from trade.views import ShopingCartViewSet, OrderInfoViewSet, AliPayView
from django.views.generic import TemplateView

# from goods.view_request_response import GoodsListViewRequestResponse
# 首页 展示路由
router = DefaultRouter()
# 注册url
router.register(r'goods', GoodsListViewSet)
router.register(r'categorys', GoodCategoryListViewSet)
# base_name:用于创建url的基础名字，如果没有设置，就根据queryset值设置，如果没有设置queryset属性，那么就必须设置base_name. 如果没有设置的话就会报错
router.register(r'code', SmsCodeViewSet, base_name='code')
router.register(r'users', UserViewSet)
router.register(r'userfavs', UserFavViewSet, base_name='userfavs')
router.register(r'messages', LeavingMessageViewSet, base_name='message')
router.register(r'address', UserAddressViewSet, base_name='address')
router.register(r'shopcarts', ShopingCartViewSet, base_name='shopcarts')
router.register(r'orders', OrderInfoViewSet, base_name='orders')
router.register(r'banners',BannerViewSet,base_name='banners')
router.register(r'indexgoods',IndexCategoryViewSet,base_name='indexgoods')

# good_list = GoodsListViewSet.as_view({
#     #get请求绑定ListModelMixin的list方法
#     'get': 'list',
# })

urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    url(r'^xadmin/', xadmin.site.urls),
    url(r'^ueditor/', include('DjangoUeditor.urls')),
    url(r'^media/(?P<path>.*)', serve, {'document_root': MEDIA_ROOT}),
    # url(r'^static/(?P<path>.*)',serve, {'document_root': STATIC_ROOT}),
    url(r'^docs/', include_docs_urls(title='硅谷商店')), # docs 文档
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api-token-auth', views.obtain_auth_token),  # token 认证
    # url(r'^jwt-token-auth',obtain_jwt_token),  # jwt 认证
    url(r'^login/$', obtain_jwt_token),  # jwt 认证
    # url(r'^goods_test/$',GoodsListViewRequestResponse.as_view(),name='goods_test'),
    # url(r'^goods/$',good_list, name='goods_list')
    url(r'^', include(router.urls)),  # 首页 展示路由
    url(r'^alipay/return', AliPayView.as_view(), name='alipay'), # 支付宝 回调
    url(r'^index/',TemplateView.as_view(template_name='index.html'),name='index'),  #前端项目
    url(r'',include('social_django.urls',namespace='social')), # 第三方登录url配置
]
