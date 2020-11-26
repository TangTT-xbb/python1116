from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.utils.decorators import method_decorator
from django.views import View

from db.base_view import VerifyLoginView
from user.forms import RegisterModelForm, LoginModelForm
from user.helper import set_password, set_session, check_login
from user.models import SpUser


class RegisterView(View):
    """
    注册视图
    """

    def get(self, request):
        return render(request, 'user/reg.html')

    def post(self, request):
        # 接收参数
        data = request.POST
        # 验证参数的合法性
        register_form = RegisterModelForm(data)
        if register_form.is_valid():
            # 操作数据库
            # 获取清洗后的数据
            cleaned_data = register_form.cleaned_data
            # 保存到数据库
            user = SpUser()
            user.phone = cleaned_data.get('phone')
            user.password = set_password(cleaned_data.get('password'))
            user.save()
            # 跳转到登录页面
            return redirect('user:登录')
        # 合成响应
        else:
            return render(request, 'user/reg.html', {'form': register_form})


class LoginView(View):
    """
    登录视图
        """

    def get(self, request):
        return render(request, 'user/login.html')

    def post(self, request):
        # 接收参数
        data = request.POST

        # 验证数据的合法性
        login_form = LoginModelForm(data)

        if login_form.is_valid():
            # 操作数据库
            # 保存登录标识到session中，单独创建一个方法保存，更新个人资料
            user = login_form.cleaned_data["user"]

            set_session(request, user)

            # 合成响应 跳转到个人中心
            return redirect('user:个人中心')
        else:
            return render(request, 'user/login.html', {'form': login_form})


class MemberView(VerifyLoginView):
    """个人中心"""

    def get(self,request):
        return render(request,'user/member.html')


    def post(self):
        return HttpResponse("hi")




