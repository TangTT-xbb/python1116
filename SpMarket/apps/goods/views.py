from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse
from django.views import View

from goods.helper import get_cart_count
from goods.models import GoodsSKU, Category
from user.models import *


class IndexView(View):
    """商品首页"""
    def get(self,request):
        return render(request, 'goods/index.html')

class DetailView(View):
    def get(self,request,id):
        # 获取商品sku信息
        goods_sku = GoodsSKU.objects.get(pk=id)
        context = {
            "goods_sku": goods_sku,
        }
        return render(request, 'goods/detail.html', context=context)



class CategoryView(View):
    """商品分类"""
    """
        1. 页面刚加载的时候 显示的商品只 显示 排序 排第一的分类下的商品
        2. 点击哪个分类 就显示 对应分类下的商品
        3. 可以按照 销量，价格(升,降)，添加时间，综合(pk) 排序 并且 是对应分类下的商品
            添加一个参数order：
                0：综合
                1：销量降
                2: 价格升
                3: 价格降
                4：添加时间降
            order_rule = ['pk', '-sale_num', 'price', '-price', '-create_time']
    """

    def get(self, request, cate_id, order):
        # 查询所有的分类
        categorys = Category.objects.filter(is_delete=False).order_by("-order")
        # 取出第一个分类
        # print(categorys[0])
        # print(categorys.first())
        if cate_id == "":
            category = categorys.first()
            cate_id = category.pk
        else:
            # 根据分类查询id查询对应的分类
            cate_id = int(cate_id)
            category = Category.objects.get(pk=cate_id)

        # 查询对应类下的所有商品
        # print(category.goodssku_set.all())
        goods_skus = GoodsSKU.objects.filter(is_delete=False, category=category)

        if order == "":
            order = 0
        order = int(order)

        # 排序规则列表
        order_rule = ['pk', '-sale_num', 'price', '-price', '-create_time']
        goods_skus = goods_skus.order_by(order_rule[order])
        # if order == 0:
        #     goods_skus = goods_skus.order_by('pk')
        # elif order == 1:
        #     goods_skus = goods_skus.order_by('-sale_num')
        # elif order == 2:
        #     goods_skus = goods_skus.order_by('price')
        # elif order == 3:
        #     goods_skus = goods_skus.order_by('-price')
        # elif order == 4:
        #     goods_skus = goods_skus.order_by('-create_time')

        # 获取 当前用户 购物车中商品的总数量
        cart_count =  get_cart_count(request)

        context = {
            'categorys': categorys,
            'goods_skus': goods_skus,
            'cate_id': cate_id,
            'cart_count':cart_count,
            'order':order,
        }

        return render(request, 'goods/category.html', context=context)
