import xadmin
from .models import Goods, GoodsCategory, GoodsImage, GoodsCategoryBrand, Banner,IndexAd


class GoodsXAdmin(object):
    list_display = ["name", "click_num", "sold_num", "fav_num", "goods_num", "market_price",
                    "shop_price", "goods_desc", "is_new", "is_hot", "add_time"]
    search_fields = ['name']
    list_filter = ['category']
    style_fields = {'goods_desc': 'ueditor'}

    class GoodImageInline(object):
        # 应用的model
        model = GoodsImage
        # 不显示的字段
        exclude = ['add_time']
        # 每次添加的数目
        extra = 1
        # 样式，表格
        style = 'tab'

    inlines = [GoodImageInline]


class GoodsCategoryAdmin(object):
    list_display = ["name", "category_type", "parent_category", "add_time"]
    search_fields = ['name']
    list_filter = ['category_type', 'parent_category', 'desc']


class GoodsCategoryBrandAdmin(object):
    list_display = ['category', 'name', 'desc', 'image']
    search_fields = ['name']
    # 实现后台添加品牌指定的商品类别只有一级类目
    def get_context(self):
        context = super(GoodsCategoryBrandAdmin,self).get_context()
        if 'form' in context:
            context['form'].fields['category'].queryset = GoodsCategory.objects.filter(category_type=1)
        return context


class GoodsImageAdmin(object):
    list_display = ['goods', 'image']


class BannerXAdmin(object):
    list_display = ['goods', 'image', 'index']

class IndexAdXAdmin(object):
   list_display = ["category", "goods", ]



xadmin.site.register(Goods, GoodsXAdmin)
xadmin.site.register(GoodsCategory, GoodsCategoryAdmin)
xadmin.site.register(GoodsCategoryBrand, GoodsCategoryBrandAdmin)
xadmin.site.register(GoodsImage, GoodsImageAdmin)
xadmin.site.register(Banner, BannerXAdmin)
xadmin.site.register(IndexAd,IndexAdXAdmin)
