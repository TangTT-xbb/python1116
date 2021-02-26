from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.


from db.base_view import VerifyLoginView


class AddCartView(VerifyLoginView):
    """操作购物车，添加购物车数据"""
    def get(self,request):
        # print(request.is_ajax())
        return HttpResponse("ok")

    def post(self):
        pass