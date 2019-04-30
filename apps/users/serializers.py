# __Author__:lizhenbin
# __time__:18/08/06,11:04
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import VerifyCode
import re
import datetime
from rest_framework.validators import UniqueValidator
from django.db.models import Q

User = get_user_model()


# 验证手机号是否可以注册的序列化器
class SMSSerializer(serializers.Serializer):
    mobile = serializers.CharField(max_length=11, min_length=11, error_messages={
        'max_length': '手机号为11位',
        'min_length': '手机号为11为'
    }, help_text='输入手机号')

    # 判断手机号是否可以注册  validate_mobile 固定写法 validate_字段名
    def validate_mobile(self, mobile):
        # 判断手机号是否存在
        if User.objects.filter(mobile=mobile):
            raise serializers.ValidationError('手机号已经存在')
        # 判断手机号是否符合规律
        if not re.match('^1[35678]\d{9}', mobile):
            raise serializers.ValidationError('手机号不合法')
        one_minutes_age = datetime.datetime.now() - datetime.timedelta(minutes=1)
        # 判断验证码的过期时间
        if VerifyCode.objects.filter(add_time__gte=one_minutes_age, mobile=mobile):
            raise serializers.ValidationError('验证码频繁发送，1分钟在发送')
        # 必须返回
        return mobile


class UserRegSerializer(serializers.ModelSerializer):
    #  因为UserProfile中没有，只能自定义,required=True:code是必须填的字段,注意一定要加上write_only=True
    # write_only=True 表示 ，以确保在更新或创建实例时可使用该字段，但序列化表示时不包含该字段(也就是返回给前端用户的时候不给该字段)
    code = serializers.CharField(label='验证码', required=True, max_length=4, min_length=4, write_only=True,
                                 error_messages={
                                     'max_length': '验证码为4位',
                                     'min_length': '验证码为4位',
                                     'required': '必填项',
                                 }, help_text='验证码')
    # 自定义 username 验证   UniqueValidator指定某一个对象是唯一的，如，用户名只能存在唯一
    username = serializers.CharField(help_text='手机号', label='用户名', required=True,
                                     validators=[UniqueValidator(queryset=User.objects.all(), message='您好，用户名不能重复')])
    # 自定义 password 验证 style={'input_type': 'password'}  输入框 为密文
    password = serializers.CharField(help_text='密码', label='密码', write_only=True, style={'input_type': 'password'})

    def validate_code(self, code):
        # self.initial_data['username']取到username 数据
        verify_codes = VerifyCode.objects.filter(mobile=self.initial_data['username']).order_by('-add_time')
        # print(self.initial_data)
        # print(self.initial_data['username'])
        if verify_codes:
            last_code = verify_codes[0]
            if last_code.code != code:
                raise serializers.ValidationError('验证码错误')
            five_minutes_ago = datetime.datetime.now() - datetime.timedelta(minutes=5)
            if last_code.add_time < five_minutes_ago:
                raise serializers.ValidationError('验证码已经过期')
            return code
        else:
            raise serializers.ValidationError('验证码错误')

    # 保存用户表 时加密 password  ,使用信号量
    # def create(self, validated_data):
    #     # 接收 默认create 方法 返回的user
    #     user = super(UserRegSerializer, self).create(validated_data=validated_data)
    #     user.set_password(validated_data['password'])
    #     user.save()
    #     # 必须返回
    #     return user

    # 保存注册后用户表的数据，不需要code,验证结束后调用
    def validate(self, attrs):
        attrs['mobile'] = attrs['username']
        del attrs['code']
        return attrs

    class Meta:
        model = User
        # 输入验证字段
        fields = ('username', 'code', 'password')  # [] 也行


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("name", "birthday", "gender", "email", "mobile")
