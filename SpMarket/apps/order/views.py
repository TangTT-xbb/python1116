from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views import View

from db.base_view import VerifyLoginView
from user.models import UserAddress


class ConfirmOrderView(VerifyLoginView):
    """ 确认订单页面"""
    def get(self,request):
        """
        1. 如果没有收货地址显示添加地址
         如果有收货地址 默认显示 默认收货地址
         如果没有默认收货地址 显示第一个

        """
        user_id = request.session.get("ID")
        address = UserAddress.objects.filter(user_id=user_id).order_by("-isDefault").first()
        # >>>> 1. 收货地址处理
        # address = None


        # 渲染数据
        context = {
            'address':address
        }




        return render(request,'order/tureorder.html',context=context)
    def post(self,request):
        return render(request,'order/tureorder.html')

class ShowOrder(VerifyLoginView):
    """确认支付页面"""
    def get(self,request):
        return render(request,'order/order.html')