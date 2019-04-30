from django.db import models
from datetime import datetime
from goods.models import Goods
from django.contrib.auth import get_user_model

# Create your models here.

User = get_user_model()


class ShopingCart(models.Model):
    user = models.ForeignKey(User, verbose_name='用户')
    goods = models.ForeignKey(Goods, verbose_name='商品')
    nums = models.IntegerField(default=0, verbose_name='商品数量')
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    def __str__(self):
        return '%s(%s)'.format(self.goods.name, self.nums)

    class Meta:
        verbose_name = '购物车'
        verbose_name_plural = verbose_name


class OrderInfo(models.Model):
    ORDER_DEFAULT = (
        ('PAYING', '待支付'),
        ('TRADE_SUCCESS', '支付成功'),
        ('TRADE_CLOSE', '支付关闭'),
        ('TRADE_FILE', '支付失败'),
        ('TRADE_FINSHED', '交易结束')
    )
    user = models.ForeignKey(User, verbose_name='用户')
    order_sn = models.CharField(max_length=30, unique=True, verbose_name='订单号', blank=True, null=True)
    trade_no = models.CharField(max_length=100, unique=True, blank=True, null=True, verbose_name='交易编号')
    pay_status = models.CharField(default='PAYING', choices=ORDER_DEFAULT, max_length=30, verbose_name='订单状态')
    post_script = models.CharField(max_length=200, verbose_name='订单留言',null=True,blank=True)
    order_mount = models.FloatField(default=0.0, verbose_name='订单金额')
    pay_time = models.DateTimeField(blank=True, null=True, verbose_name='支付时间')
    signer_name = models.CharField(max_length=30, verbose_name='签收人')
    signer_mobile = models.CharField(max_length=11, verbose_name='联系电话')
    address = models.CharField(max_length=200, verbose_name='收货地址')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='创建时间')

    def __str__(self):
        return str(self.order_sn)

    class Meta:
        verbose_name = '订单信息'
        verbose_name_plural = verbose_name


class OrderGoods(models.Model):
    order = models.ForeignKey(OrderInfo, verbose_name='订单', related_name='goods')
    goods = models.ForeignKey(Goods, verbose_name='商品')
    good_nums = models.IntegerField(default=0, verbose_name='商品数量')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    def __str__(self):
        return str(self.order.order_sn)

    class Meta:
        verbose_name = '订单商品信息'
        verbose_name_plural = verbose_name
