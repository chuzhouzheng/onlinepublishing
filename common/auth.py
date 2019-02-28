__author__ = 'Administrator'

'''
    1.用户认证，auth_user表里的用户才能登录并校验token
    2.权限认证，超级管理员才有权限访问
    3.频率认证,每秒访问次数不能超过10次
'''

from rest_framework.authentication import BaseAuthentication
from rest_framework.permissions import BasePermission
from rest_framework.throttling import BaseThrottle
from rest_framework import exceptions
from rest_framework.parsers import JSONParser
from storybook.models import UserToken
from django.contrib.auth.models import User


class UserAuthentication(BaseAuthentication):
    '''
        认证组件，校验token，auth_user表里的用户
    '''

    def authenticate(self, request):
        token = request.GET.get('token')
        token_obj = UserToken.objects.filter(token=token).first()
        if not token_obj:
            raise exceptions.AuthenticationFailed("Token校验失败！")
        return token_obj.user.username, token_obj.token


class UserPermission(BasePermission):
    '''
        权限组件，auth_user表里的用户权限is_superuser
        message:错误信息
        request.user是用户名，是在Authentication类返回的（oken_obj.user.username）
    '''
    message = ""
    def has_permission(self, request, views):

        if User.objects.filter(username=request.user).first().is_superuser:
            return True
        else:
            self.message = "权限不足，超级管理员才能访问"
            return False


class UserThrottle(BaseThrottle):
    '''
        频率组件
    '''
    def allow_request(self, request, views):
        pass
    def wait(self):
        pass