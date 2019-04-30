from django.db import models
from django.contrib.auth import get_user_model
from goods.models import Goods
from datetime import datetime

# Create your models here.

User = get_user_model()


class UserFav(models.Model):
    user = models.ForeignKey(User, verbose_name='用户')
    goods = models.ForeignKey(Goods, verbose_name='商品')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')


    def __str__(self):
        return '%s收藏了%s'.format(self.user.name, self.goods.goods_sn)

    class Meta:
        verbose_name = "用户收藏"
        verbose_name_plural = verbose_name
        unique_together = ('user','goods')


class UserLeavingMessage(models.Model):
    MSG_TYPE = (
        (1, "留言"),
        (2, "投诉"),
        (3, "询问"),
        (4, "售后"),
        (4, "求购"),

    )
    user = models.ForeignKey(User, verbose_name='用户')
    subject = models.CharField(max_length=100, default='', verbose_name='留言主题')
    msg_type = models.IntegerField(choices=MSG_TYPE, default=1, verbose_name='留言类型',
                                   help_text='留言类型: 1(留言),2(投诉),3(询问),4(售后),5(求购)')
    message = models.CharField(max_length=500, verbose_name='留言内容')
    file = models.FileField(upload_to='message/images/', verbose_name='上传的文件', help_text='上传的文件')
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    def __str__(self):
        return '%s留言%s'.format(self.user.name, self.subject)

    class Meta:
        verbose_name = '用户留言'
        verbose_name_plural = verbose_name


class UserAddress(models.Model):
    user = models.ForeignKey(User, verbose_name="用户")
    province = models.CharField(max_length=50, default="", verbose_name="省")
    city = models.CharField(max_length=50, verbose_name="市")
    district = models.CharField(max_length=100, verbose_name="区")
    address = models.CharField(max_length=200, verbose_name="地址", default="")
    signer_name = models.CharField(max_length=30, verbose_name="签收人")
    signer_mobile = models.CharField(max_length=11, verbose_name="联系电话")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    def __str__(self):
        return self.address

    class Meta:
        verbose_name = "收货地址"
        verbose_name_plural = verbose_name
