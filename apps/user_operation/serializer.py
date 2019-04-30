from rest_framework import serializers
from goods.serializers import GoodsSerializer
from .models import UserFav, UserLeavingMessage, UserAddress
from rest_framework.validators import UniqueTogetherValidator


# 用户收藏 create
class UserFavSerializer(serializers.ModelSerializer):
    # 校验user 指定用户为当前用户
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        # 联合唯一 实现一个商品只能同一个用户收藏一次,也可以 在model中class Meta:  unique_together = ('user','goods')
        validators = [
            UniqueTogetherValidator(queryset=UserFav.objects.all(), fields=('user', 'goods'), message='重复收藏')
        ]
        model = UserFav
        fields = ('user', 'goods')


#  用户收藏 详情序列化器 list
class UserFavDetailSerializer(serializers.ModelSerializer):
    goods = GoodsSerializer()

    class Meta:
        model = UserFav
        fields = ('goods', 'id')


class LeavingMessageSerializers(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    # read_only=True 表示不需填写该字段,默认添加时间(现在)序列化json给前端
    add_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M', help_text='添加时间')

    class Meta:
        model = UserLeavingMessage
        fields = ("user", "subject", "msg_type", "message", "file", "add_time", "id")


class UserAddressSerializers(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    add_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M')

    class Meta:
        model = UserAddress
        fields = ("id", "user", "province", "city", "district", "address", "signer_name", "signer_mobile", "add_time")
