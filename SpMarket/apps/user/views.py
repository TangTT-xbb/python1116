from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views import View


class LoginView(View):
    """
    登录视图
        """

    def get(self, requset):
        return render(requset, 'user/login.html')

    def post(self, requset):
        pass
