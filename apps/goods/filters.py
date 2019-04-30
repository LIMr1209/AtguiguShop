from django_filters import rest_framework as filters
from .models import Goods
from django.db.models import Q


# 创建 自定义 过滤器
# class GoodsFilter(filters.FilterSet):
#     # 最低价格
#     min_price = filters.NumberFilter(field_name="shop_price", lookup_expr='gte')  # 大于等于
#     # 最大价格
#     max_price = filters.NumberFilter(field_name="shop_price", lookup_expr='lte')  # 小于等于
#
#     name = filters.CharFilter(field_name='name', lookup_expr='icontains')  # 包含
#
#     class Meta:
#         model = Goods
#         fields = ['min_price', 'max_price']
# 根据前端创建自定义过滤器
class GoodsFilter(filters.FilterSet):
    pricemin = filters.NumberFilter(field_name='shop_price', lookup_expr='gte', help_text='最小价格')
    pricemax = filters.NumberFilter(field_name='shop_price', lookup_expr='lte', help_text='最大价格')
    name = filters.CharFilter(field_name="name", lookup_expr="icontains", help_text='根据商品名过滤商品列表')
    top_category = filters.NumberFilter(method='top_category_filters', help_text='根据商品类目过滤商品列表')
    is_hot = filters.BooleanFilter(help_text='是否热卖')
    is_new = filters.BooleanFilter(help_text='是否新品')

    # name  是 top_category 这个字段
    # value 是商品类别的id
    # queryset 是商品数据
    def top_category_filters(self, queryset, name, value):
        # 商品数据根据它的商品三级类目或二级类目或三级类目进行过滤
        queryset = queryset.filter(Q(category__id=value) | Q(category__parent_category_id=value) | Q(
            category__parent_category__parent_category_id=value))
        print(queryset)
        return queryset

    class Meta:
        model = Goods
        fields = ['pricemin', 'pricemax', 'name', 'is_hot', 'is_new']
