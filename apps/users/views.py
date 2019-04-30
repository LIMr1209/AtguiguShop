from django.shortcuts import render
from django.db.models import Q
from django.contrib.auth.backends import get_user_model, ModelBackend
from rest_framework import mixins, status
from rest_framework.response import Response
from rest_framework import viewsets
from .serializers import SMSSerializer, UserRegSerializer, UserDetailSerializer
from .models import VerifyCode
from random import randint
from utils.yunpian import YunPian
from rest_framework_jwt.utils import jwt_encode_handler, jwt_payload_handler
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated

# Create your views here.
User = get_user_model()


# 自定义用户登录方式
class CustomModelBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # 找到用户  Q对象 或者的关系
            user = User.objects.filter(Q(username=username) | Q(mobile=username))[0]
            # 校验密码
            if user.check_password(password):
                return user
        except Exception as e:
            # 找不到返回None
            return None


# 发送验证码，保存验证码
class SmsCodeViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    '''
    create:
        获取验证码
    '''
    serializer_class = SMSSerializer

    # 如果没有设置queryset属性，那么url  router.register就必须设置base_name. 如果没有设置的话就会报错
    # queryset = VerifyCode.objects.all()
    #   CreateModelMixin 的 create 方法重写
    def random_code(self):
        a = '1234567890'
        code = ''
        for i in range(4):
            code += a[randint(0, len(a) - 1)]
        return code

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        # print(serializer)
        # print(SmsCodeViewSet.serializer_class)
        # 校验序列化器的 validate_mobile 方法
        serializer.is_valid(raise_exception=True)
        # 取出 mobile
        mobile = serializer.data['mobile']
        code = self.random_code()
        yp = YunPian()
        # sms_status  {'code': 0, 'msg': '发送成功', 'count': 1, 'fee': 0.05, 'unit': 'RMB', 'mobile': '17635700440', 'sid': 26748214808}
        sms_status = yp.send_msg('17635700440', code)
        print(sms_status)
        if sms_status['code'] == 0:
            VerifyCode(mobile=mobile, code=code).save()
            return Response({
                'mobile': mobile,
                'msg': sms_status['msg'],
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                'mobile': mobile,
                'msg': sms_status['msg'],
            }, status=status.HTTP_400_BAD_REQUEST)
        # 保存验证码
        # self.perform_create(serializer)
        # headers = self.get_success_headers(serializer.data)
        # return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class UserViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin):
    '''
    create:
        注册用户
    retrieve:
        得到当前用户信息
    update:
        更新当前用户信息
    '''
    queryset = User.objects.all()
    # serializer_class = UserRegSerializer
    # 认证 JWT ,和 session
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    # 使用 user/\d/  取到的用户始终是当前用户
    def get_object(self):
        return self.request.user

    # 动态设置permissions(权限)
    def get_permissions(self):
        # 当使用 user/\d/  获取用户时,返回是否登录权限
        if self.action == 'retrieve':
            return [IsAuthenticated()]
        # 当注册的时候,不需权限
        elif self.action == 'created':
            return []
        return []

    # 动态设置序列化器
    def get_serializer_class(self):
        # 当注册的时候使用注册序列化器
        if self.action == 'create':
            return UserRegSerializer
        # 当删除用户,修改,获取用户的时候使用用户详情序列化器
        else:
            return UserDetailSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        response = serializer.data
        payload = jwt_payload_handler(user)
        # 适应前端 返回name
        response['name'] = user.name if user.name else user.username
        # 注册用户时,给JWT
        response['token'] = jwt_encode_handler(payload)
        headers = self.get_success_headers(serializer.data)
        return Response(response, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        return serializer.save()
