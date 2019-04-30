from django.db.models import Q
from rest_framework import serializers
from .models import Goods, GoodsCategory, GoodsImage, Banner, GoodsCategoryBrand,IndexAd


# 序列化器


class GoodsCategorySerializer3(serializers.ModelSerializer):
    class Meta:
        model = GoodsCategory
        fields = '__all__'


class GoodsCategorySerializer2(serializers.ModelSerializer):
    # sub_cat 是 related_name  的值  二级类目展示三级类目  ,一对多关系指定many=True
    sub_cat = GoodsCategorySerializer3(many=True)

    class Meta:
        model = GoodsCategory
        fields = '__all__'


class GoodsCategorySerializer1(serializers.ModelSerializer):
    # 一级类目展示二级类目
    sub_cat = GoodsCategorySerializer2(many=True)

    class Meta:
        model = GoodsCategory
        fields = '__all__'


class GoodsImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsImage
        fields = ('image',)  # The `fields` option must be a list or tuple or "__all__".


class GoodsSerializer(serializers.ModelSerializer):
    # 外键数据的展示  商品展示三级类目    多对一关系，多找一 不需指定many=true
    category = GoodsCategorySerializer3()
    images = GoodsImageSerializer(many=True)

    class Meta:
        # 指定 model
        model = Goods
        # 显示全部字段
        fields = '__all__'


# 首页轮播
class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = '__all__'


# 品牌序列化
class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsCategoryBrand
        fields = '__all__'


# 首页类别数据展示
class IndexCategorySerializer(serializers.ModelSerializer):
    # 一对多关系 商品类别对商品品牌
    brands = BrandSerializer(many=True)

    # 二级类目，三级类目的展示 一对多关系
    sub_cat = GoodsCategorySerializer2(many=True)

    # 首页类目商品广告
    ad_goods = serializers.SerializerMethodField()

    def get_ad_goods(self, obj):
        data = {}
        ad_goods = IndexAd.objects.filter(category=obj)
        if ad_goods:
            goods = ad_goods[0].goods
            goods_serializer = GoodsSerializer(goods,context={'request':self.context['request']})
            data = goods_serializer.data
        return data

    # 得到 GoodsCategory '生鲜食品','酒水饮料' 商品类别的所有商品
    goods = serializers.SerializerMethodField()

    def get_goods(self, obj):
        # obj 为 IndexCategorySerializer 的实例 ，也就是商品类别 GoodsCategory 的实例
        all_goods = Goods.objects.filter(Q(category_id=obj.id) | Q(category__parent_category_id=obj.id) | Q(
            category__parent_category__parent_category_id=obj.id))
        # 序列化 得到的商品 一对多， context 添加前缀 http:127.0.0.1:8000
        goods_serializer = GoodsSerializer(all_goods, many=True, context={'request': self.context['request']})
        # 返回序列化的数据
        return goods_serializer.data

    class Meta:
        model = GoodsCategory
        fields = '__all__'
