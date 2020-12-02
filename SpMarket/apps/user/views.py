import random
import re

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.utils.decorators import method_decorator
from django.views import View

from db.base_view import VerifyLoginView
from user.forms import RegisterModelForm, LoginModelForm, ForgetpwdModelForm, UpdatepwdModelForm
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

    def get(self, request):
        return render(request, 'user/member.html')

    def post(self):
        return HttpResponse("hi")


class ForgetpwdView(View):
    def get(self, request):
        return render(request, 'user/forgetpassword.html')

    def post(self, request):
        # 接收数据
        data = request.POST
        # 验证数据合法性
        forgetpwd_form = ForgetpwdModelForm(data)
        if forgetpwd_form.is_valid():
            # 操作数据库
            # 更新密码到数据库
            cleaned_data = forgetpwd_form.cleaned_data
            # 保存到数据库
            phone = cleaned_data.get('phone')
            password = set_password(cleaned_data.get('password'))
            # 修改密码保存到数据库
            user = SpUser.objects.get(phone=phone)
            user.password = password
            user.save()

            # 跳转到登录
            return redirect('user:登录')

        # 合成响应
        context = {

            'form': forgetpwd_form
        }
        return render(request, 'user/forgetpassword.html', context=context)


class UpdatepwdView(VerifyLoginView):
    def get(self, request):
        return render(request, 'user/password.html')

    def post(self, request):
        # 接收数据
        data = request.POST

        # 验证数据合法性
        updatepwd_form = UpdatepwdModelForm(data)
        if updatepwd_form.is_valid():
            cleaned_data = updatepwd_form.cleaned_data
            # 保存到数据库

            phone = request.session['phone']
            password = set_password(cleaned_data.get('password'))
            # 第一种
            # SpUser.objects.filter(phone=phone).update(password=password)
            # 第二种
            user = SpUser.objects.get(phone=phone)
            user.password = password
            user.save()
            # 合成响应
            return redirect('user:登录')


        else:
            return render(request, 'user/password.html', {'form': updatepwd_form})


def saftystep(request):
    phone = request.session['phone']
    context = {
        'phone': phone
    }
    return render(request, 'user/saftystep.html', context=context)


# 验证码随机
# i = [random.randint(0,9) for _ in range(6)]

class SendMsg(View):
    def get(self, request):
        pass

    def post(self, request):
        # 接收数据
        phone = request.POST.get("phone", '')
        rs = re.search('^1[3-9]\d{9}$', phone)
        if rs is None:
            return JsonResponse({'error': 1, 'errorMsg': '手机号码格式错误！'})
        # 处理数据
        """
        1. 生成随机验证码
        2. 
        3. 接入运营商
        
        
        """
        random_code = "".join([str(random.randint(0, 9)) for _ in range(6)])

        # 合成响应
        return JsonResponse({'error': 0})
