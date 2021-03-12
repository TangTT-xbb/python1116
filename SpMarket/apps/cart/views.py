from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

from cart.helper import json_msg, get_cart_key, get_cart_count
from db.base_view import VerifyLoginView
from goods.models import GoodsSKU
from django_redis import get_redis_connection


class AddCartView(VerifyLoginView):
    """操作购物车, 添加购物车数据"""
    """
        1. 需要接收的参数
            sku_id count 
            从session中获取用户id

        2. 验证参数合法性
            a. 判断 为整数
            b. 要在数据库中存在商品
            c. 验证库存是否充足

        3. 操作数据库
            将购物车 保存到redis
            存储的时候采用的数据库类型为hash
            key           field value  field value
            cart_user_id  sku_id count

    """

    def post(self, request):
        # 1. 接收参数
        user_id = request.session.get("ID")
        sku_id = request.POST.get("sku_id")
        count = request.POST.get("count")

        # a.判断为整数
        try:
            sku_id = int(sku_id)
            count = int(count)
        except:
            return JsonResponse(json_msg(1, "参数错误!"))
        # b.要在数据库中存在商品
        try:
            goods_sku = GoodsSKU.objects.get(pk=sku_id)
        except GoodsSKU.DoesNotExist:
            return JsonResponse(json_msg(2, "商品不存在!"))

        # 判断库存
        if goods_sku.stock < count:
            return JsonResponse(json_msg(3, "库存不足!"))

        # 2. 操作数据
        # 创建连接
        r = get_redis_connection()
        # 处理购物车的 key
        cart_key = get_cart_key(user_id)

        # 添加
        # 获取购物车中已经存在的数量 加 上 需要添加 与 库存进行比较
        old_count = r.hget(cart_key, sku_id)  # 二进制
        if old_count is None:
            old_count = 0
        else:
            old_count = int(old_count)

        if goods_sku.stock < old_count + count:
            return JsonResponse(json_msg(3, "库存不足!"))

        # 将商品添加到购物车
        # r.hset(cart_key,sku_id,old_count + count)
        # ctrl + shift + u
        rs_count = r.hincrby(cart_key, sku_id, count)
        if rs_count <= 0:
            # 删除field
            r.hdel(cart_key, sku_id)

        # 获取购物车中的总数量
        cart_count = get_cart_count(request)

        # 3. 合成响应
        return JsonResponse(json_msg(0, "添加购物车成功", data=cart_count))


class CartShowView(VerifyLoginView):
    """购物车展示"""

    def get(self, request):
        """
        步骤
            1. 从redis获取所有的购物车信息(sku_id,count)
            2. 根据购物中的sku_id从 商品sku表中获取商品信息
            3. 渲染的数据
                将购物车中数量和商品信息合成一块儿
        """
        # 1. 接收参数
        user_id = request.session.get("ID")
        # 2. 操作数据库
        r = get_redis_connection()
        # 准备键
        cart_key = get_cart_key(user_id)

        # 从redis获取所有的购物车信息
        cart_datas = r.hgetall(cart_key)
        # 准备一个空列表,保存多个商品
        goods_skus = []
        # 遍历字典
        for sku_id, count in cart_datas.items():
            # 将二进制数据转成整型
            sku_id = int(sku_id)
            count = int(count)

            # 2. 根据购物中的sku_id从 商品sku表中获取商品信息
            try:
                goods_sku = GoodsSKU.objects.get(pk=sku_id, is_delete=False, is_on_sale=True)
            except GoodsSKU.DoesNotExist:
                # 删除redis中过期的数据
                r.hdel(cart_key, sku_id)
                continue
            if count <= 0:
                r.hdel(cart_key, sku_id)
                continue
            # 3. 将购物车中数量和商品信息合成一块儿(给一个已经存在的对象添加属性)
            goods_sku.count = count
            # setattr(goods_sku,'count',count)

            # 保存商品到商品列表
            goods_skus.append(goods_sku)

        # 渲染数据
        context = {
            'goods_skus': goods_skus
        }

        return render(request, 'cart/shopcart.html', context=context)

