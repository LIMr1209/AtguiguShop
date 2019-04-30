from rest_framework.permissions import BasePermission
from rest_framework import permissions


# 自定义的权限
class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        # 如果 request 请求为 SAFE_METHODS = ('GET', 'HEAD', 'OPTIONS') 则给权限
        if request.method in permissions.SAFE_METHODS:
            return True
        # 如果为 post delete update 则判断登陆用户和请求用户是否是同一个用户，是的话给权限
        return obj.user == request.user