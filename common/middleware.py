__author__ = 'Administrator'

from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect, render
from django.contrib import auth
from Django_sample.settings import LOGIN_URL


class CheckSession(MiddlewareMixin):
    '''Session校验'''

    def __str__(self):
        return '<CheckSession Object>'

    def process_request(self, request):
        # print(request)
        # print(request.user,type(request.user))
        assert hasattr(request, 'user')
        if not request.user.is_authenticated:
            if '/storybook/FBV/' in request.path_info:
                print('session 校验不通过！')
                if request.path_info in '/storybook/FBV/login/' and request.method == "POST":
                    return None
                else:
                    return render(request, 'storybook/login.html')