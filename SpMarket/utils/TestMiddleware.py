from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin


class TestMiddleware(MiddlewareMixin):
    def process_request(self,request):
        # 可以返回None  或者返回response对象
        # 判断是否是微信浏览器
        if request.META.get('HTTP_USER_AGENT').find('MicroMessenger') == -1:
            return HttpResponse("非微信浏览器使用")

        return None