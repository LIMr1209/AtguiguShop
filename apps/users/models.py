from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime


# Create your models here.

class UserProfile(AbstractUser):
    # help_text 在自动生成文档的时候用到
    name = models.CharField(max_length=30, verbose_name='姓名', null=True,blank=True, help_text='姓名')
    birthday = models.DateField(null=True, blank=True, verbose_name='出生年月', help_text='出生年月')
    gender = models.CharField(choices=(('male', '男'), ('female', '女')), max_length=10, verbose_name='性别',
                              default='female',
                              help_text='性别')
    mobile = models.CharField(max_length=11, verbose_name='电话', help_text='电话')
    email = models.EmailField(max_length=100, verbose_name='邮箱', null=True, blank=True, help_text='邮箱')

    def __str__(self):
        if self.name:
            return self.name
        else:
            return self.username

    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name


class VerifyCode(models.Model):
    code = models.CharField(max_length=11, verbose_name='短信验证码', help_text='短信验证码')
    mobile = models.CharField(max_length=11, verbose_name='电话', help_text='电话')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间', help_text='添加时间')

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = '短信验证码'
        verbose_name_plural = verbose_name
