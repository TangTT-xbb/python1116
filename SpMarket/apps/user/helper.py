import hashlib

from django.http import JsonResponse
from django.shortcuts import redirect

from SpMarket.settings import SECRET_KEY, ACCESS_KEY_ID, ACCESS_KEY_SECRET
from aliyunsdkdysmsapi.request.v20170525 import SendSmsRequest
from aliyunsdkcore.client import AcsClient

from aliyunsdkcore.profile import region_provider

from cart.helper import json_msg


def set_password(password):
    # 循环加密+加盐

    for _ in range(1000):
        pass_str = "{}{}".format(password, SECRET_KEY)
        h = hashlib.md5(pass_str.encode('utf-8'))
        password = h.hexdigest()
    # 返回加密后的密码
    return password


def set_session(request, user):
    request.session['ID'] = user.pk
    request.session['phone'] = user.phone  # 使用session来保存用户登录信息
    request.session['head'] = user.head
    request.session.set_expiry(None)  # 两周
    # request.session.set_expiry(0)  # 关闭浏览器就消失


def check_login(func):  # 登录验证装饰器
    # 新函数
    def verify_login(request, *args, **kwargs):
        # 验证session中是否有登录标识
        if request.session.get("ID") is None:
            # 将上个请求地址保存到session
            referer = request.META.get('HTTP_REFERER',None)
            if referer:
                request.session['referer'] = referer


            # 判断是否为ajax请求
            if request.is_ajax():
                # 是ajax请求 提示
                return JsonResponse(json_msg(1,'未登录'))
            else:
                # 跳转到登录
                return redirect('user:登录')
        else:  # 调用原函数
            return func(request, *args, **kwargs)
        # 返回新函数

    return verify_login


# 发送短信
REGION = "cn-hangzhou"
PRODUCT_NAME = "Dysmsapi"
DOMAIN = "dysmsapi.aliyuncs.com"
acs_client = AcsClient(ACCESS_KEY_ID, ACCESS_KEY_SECRET, REGION)
region_provider.add_endpoint(PRODUCT_NAME, REGION, DOMAIN)


# 完成
def send_sms(business_id, phone_numbers, sign_name, template_code, template_param=None):
    smsRequest = SendSmsRequest.SendSmsRequest()
    # 申请的短信模板编码,必填
    smsRequest.set_TemplateCode(template_code)

    # 短信模板变量参数
    if template_param is not None:
        smsRequest.set_TemplateParam(template_param)

    # 设置业务请求流水号，必填。
    smsRequest.set_OutId(business_id)

    # 短信签名
    smsRequest.set_SignName(sign_name)

    # 数据提交方式
    # smsRequest.set_method(MT.POST)

    # 数据提交格式
    # smsRequest.set_accept_format(FT.JSON)

    # 短信发送的号码列表，必填。
    smsRequest.set_PhoneNumbers(phone_numbers)

    # 调用短信发送接口，返回json
    smsResponse = acs_client.do_action_with_exception(smsRequest)

    # TODO 业务处理

    return smsResponse
