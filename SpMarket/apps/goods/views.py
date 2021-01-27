from django.shortcuts import render

# Create your views here.

from user.models import *

def goodsindexview(request):
    return render(request,'goods/index.html')