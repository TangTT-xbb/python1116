from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse
from django.views import View

from goods.models import GoodsSKU
from user.models import *


def goodsindex(request):
    return render(request, 'goods/index.html')


def goodsdetail(request, q):
    id = q
    data = GoodsSKU.objects.get(id=id)
    # price = data['price']
    context={
        "data":data,
    }
    return render(request,'goods/detail.html',context=context)

def category(request):
    return render(request,'goods/category.html')


