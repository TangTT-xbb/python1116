import random
import re
import uuid

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.utils.decorators import method_decorator
from django.views import View

from db.base_view import VerifyLoginView
from user.forms import RegisterModelForm, LoginModelForm, ForgetpwdModelForm, UpdatepwdModelForm
from user.helper import set_password, set_session, check_login, send_sms
from user.models import SpUser
from django_redis import get_redis_connection


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
        2. 保存发送的验证码用于注册的表单验证
        3. 接入运营商    
        """
        random_code = "".join([str(random.randint(0, 9)) for _ in range(6)])
        print("=========随机验证码为：{}============".format(random_code))
        # 接入运营商
        # 保存发送的验证码到redis
        # 获取连接
        r = get_redis_connection()
        # 保存手机号码对应的验证码
        r.set(phone, random_code)
        # 设置过期时间
        r.expire(phone, 60)
        # 保存手机号码发送的次数
        key_times = "{}_times".format(phone)
        now_times = r.get(key_times)  # 从redis获取的二进制，需要转换
        if now_times is None or int(now_times) < 5:
            r.incr(key_times)
            # 设置一个过期时间
            r.expire(key_times, 360)

        else:
            # 返回并告知用户发送次数过多
            return JsonResponse({'error': 1, "errorMsg": "验证码发送次数过多"})

        # >> > 3.
        # 接入运营商
        __business_id = uuid.uuid1()
        params = "{\"code\":\"%s\"}" % random_code
        print(params)

        rs = send_sms(__business_id, phone, "唐红艳", "SMS_206538704", params)
        # rs = send_sms(__business_id, 手机号码, "签名名称", "模板code", 传入参数)
        print(rs.decode('utf-8'))

        # 合成响应
        return JsonResponse({'error': 0})


class InfoView(VerifyLoginView):
    def get(self, request):
        # 获取用户session中的id
        user_id = request.session.get('ID')
        # 获取用户信息
        user = SpUser.objects.get(pk=user_id)
        # 渲染页面
        context = {
            'user': user,
        }
        return render(request, 'user/infor.html', context=context)

    def post(self, request):
        # 接收参数
        data = request.POST
        head = request.FILES.get('head')
        user_id = request.session.get('ID')
        user = SpUser.objects.get(pk=user_id)
        user.nickname = data.get('nickname')
        user.gender = data.get('gender')
        if head is not None:
            user.head = head
        user.save()
        # 操作数据库
        # 修改session
        set_session(request, user)
        # 合成响应
        return redirect('user:个人中心')



