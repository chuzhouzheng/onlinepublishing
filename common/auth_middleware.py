__author__ = 'Administrator'

from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect, render



class CheckSession(MiddlewareMixin):
    '''Session校验'''

    def __str__(self):
        return '<CheckSession Object>'

    def process_request(self, request):
        # print(request)
        # print(request.user,type(request.user))
        assert hasattr(request, 'user')
        if not request.user.is_authenticated:
            if request.path_info in '/publish/login/' and request.method == "POST":
                return None
            else:
                return render(request, 'login.html')