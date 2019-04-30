from django.db import models
from datetime import datetime
from DjangoUeditor.models import UEditorField


# Create your models here.

class GoodsCategory(models.Model):
    CATEGORY_TYPE = (
        (1, '一级类目'),
        (2, '二级类目'),
        (3, '三级类目'),
    )
    name = models.CharField(max_length=30, default='', verbose_name='类别名', help_text='类别名')
    code = models.CharField(max_length=30, default='', verbose_name='类别code')
    desc = models.TextField(default='', verbose_name='类别描述')
    category_type = models.IntegerField(choices=CATEGORY_TYPE, verbose_name="类目级别", help_text="类目级别", null=True,
                                        blank=True)
    parent_category = models.ForeignKey('self', related_name='sub_cat', null=True, blank=True, verbose_name='父类目',
                                        help_text='父类目')
    is_tab = models.BooleanField(default=False, verbose_name='是否导航', help_text='是否导航')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间', help_text='添加时间')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '商品类别'
        verbose_name_plural = verbose_name


class GoodsCategoryBrand(models.Model):
    category = models.ForeignKey(GoodsCategory, related_name='brands', null=True, blank=True, verbose_name='商品类目',
                                 help_text='商品类目')
    name = models.CharField(default='', max_length=30, verbose_name='品牌名称', help_text='品牌名称')
    desc = models.CharField(default='', max_length=100, verbose_name='品牌描述', help_text='品牌描述')
    image = models.ImageField(max_length=200, upload_to='brand/images', verbose_name='品牌图片', help_text='品牌图片')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间', help_text='添加时间')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '品牌名'
        verbose_name_plural = verbose_name


class Goods(models.Model):
    category = models.ForeignKey(GoodsCategory, null=True, blank=True, verbose_name='商品类目', help_text='商品类目')
    goods_sn = models.CharField(max_length=50, default="", null=True, blank=True, verbose_name="商品唯一货号")
    name = models.CharField(max_length=100, verbose_name="商品名称")
    click_num = models.IntegerField(default=0, verbose_name="点击数")
    sold_num = models.IntegerField(default=0, verbose_name="销售量")
    fav_num = models.IntegerField(default=0, verbose_name="收藏数")
    goods_num = models.IntegerField(default=0, verbose_name="库存数")
    market_price = models.FloatField(default=0.0, verbose_name="市场价格")
    shop_price = models.FloatField(default=0.0, verbose_name="本店价格")
    goods_brief = models.TextField(max_length=500, verbose_name="商品简明描述")
    goods_desc = UEditorField(verbose_name=' ', width=1000, height=300, imagePath="goods/images/",
                              filePath="goods/files/", default="", upload_settings={'imageMaxSizing': 1024000})
    ship_free = models.BooleanField(default=True, verbose_name='是否承担运费')
    goods_front_image = models.ImageField(upload_to='goods/images/', verbose_name='封面图', null=True, blank=True)
    is_hot = models.BooleanField(default=False, verbose_name='是否热卖')
    is_new = models.BooleanField(default=True, verbose_name='是否新品')
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '商品信息'
        verbose_name_plural = verbose_name


class GoodsImage(models.Model):
    goods = models.ForeignKey(Goods, verbose_name='轮播商品', related_name='images', help_text='轮播商品')
    image = models.ImageField(upload_to='goods/goodimages', verbose_name='图片', null=True, blank=True)
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间', help_text='添加时间')

    def __str__(self):
        return self.goods.name

    class Meta:
        verbose_name = '商品图片轮播'
        verbose_name_plural = verbose_name


class Banner(models.Model):
    goods = models.ForeignKey(Goods, verbose_name='轮播商品')
    image = models.ImageField(upload_to='goods/banner', verbose_name='轮播图片')
    index = models.IntegerField(default=0, verbose_name='轮播顺序')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    def __str__(self):
        return self.goods.name

    class Meta:
        verbose_name = '首页轮播'
        verbose_name_plural = verbose_name


class IndexAd(models.Model):
    category = models.ForeignKey(GoodsCategory, null=True, blank=True, verbose_name='商品类目')
    goods = models.ForeignKey(Goods, verbose_name="商品")

    class Meta:
        verbose_name = '首页类目商品广告'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.goods.name
