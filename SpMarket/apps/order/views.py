from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views import View


class ConfirmOrderView(View):
    def get(self,request):
        pass
    def post(self,request):
        return HttpResponse('ok')