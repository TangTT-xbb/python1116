from datetime import datetime
import random

from django.db import transaction
from django.http import HttpResponse, Http404, JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.views import View

from django_redis import get_redis_connection

from cart.helper import get_cart_key, json_msg
from db.base_view import VerifyLoginView
from goods.models import GoodsSKU
from order.models import Transport, Order, OrderGoods
from user.models import UserAddress, SpUser


class ConfirmOrderView(VerifyLoginView):
    """ 确认订单页面"""

    def get(self, request):
        """
        1. 如果没有收货地址显示添加地址
         如果有收货地址 默认显示 默认收货地址
         如果没有默认收货地址 显示第一个

         2. 展示商品信息
            a. 获取商品sku_ids
             如何获取多个参数的值 getlist() get()只能获取一个

             b. 根据商品id获取商品信息 获取购物车中商品数量redis

        """
        user_id = request.session.get("ID")
        address = UserAddress.objects.filter(user_id=user_id).order_by("-isDefault").first()
        # >>>> 1. 收货地址处理
        # address = None
        #
        sku_ids = request.GET.getlist("sku_ids")
        # 准备空列表 装商品
        goods_skus = []

        # 准备商品总价
        goods_total_price = 0

        # 准备redis
        r = get_redis_connection()
        # 准备键
        cart_key = get_cart_key(user_id)

        for sku_id in sku_ids:
            # 商品信息
            try:
                goods_sku = GoodsSKU.objects.get(pk=sku_id)
            except GoodsSKU.DoesNotExist:
                return redirect("cart:购物车展示")
                # raise Http404("购物 车商品不存在")

            # 获取对应商品的数量
            try:
                count = r.hget(cart_key, sku_id)
                count = int(count)
            except:
                # 商品不存在就返回购物车页面
                return redirect("cart:购物车展示")
            # 保存到商品对象上
            goods_sku.count = count

            goods_skus.append(goods_sku)

            goods_total_price += (goods_sku.price * goods_sku.count)
            # print(goods_total_price)

        # 获取运输方式
        transports = Transport.objects.filter(is_delete=False).order_by('price')

        # 渲染数据
        context = {
            'address': address,
            'goods_skus': goods_skus,
            'goods_total_price': goods_total_price,
            'transports': transports,
        }

        return render(request, 'order/tureorder.html', context=context)

    @transaction.atomic
    def post(self, request):
        """
        保存订单数据
        1. 订单基本信息表 和 订单商品表

        """
        # 1. 接收参数
        transport_id = request.POST.get("transport")
        address_id = request.POST.get("address")
        sku_ids = request.POST.getlist("sku_ids")

        user_id = request.session.get("ID")
        user = SpUser.objects.get(pk=user_id)
        # 验证数据合法性
        try:
            transport_id = int(transport_id)
            address_id = int(address_id)
            sku_ids = [int(i) for i in sku_ids]
        except:
            return JsonResponse(json_msg(2, "数据不合法"))

        # 验证收货地址和运输方式存在
        try:
            address = UserAddress.objects.get(pk=address_id)
        except UserAddress.DoesNotExist:
            return JsonResponse(json_msg(3, "收货地址不存在"))
        try:
            transport = Transport.objects.get(pk=transport_id)
        except Transport.DoesNotExist:
            return JsonResponse(json_msg(4, "运输方式不存在"))

        # 2. 操作数据
        # 创建保存点
        sid = transaction.savepoint()



        #  操作订单基本信息表
        order_sn = "{}{}{}".format(datetime.now().strftime("%Y%m%d%H%M%S"), user_id, random.randrange(10000, 99999))
        address_info = "{}{}{}-{}".format(address.hcity, address.hproper, address.harea, address.brief)
        try:
            order = Order.objects.create(
                user=user,
                order_sn=order_sn,
                transport_price=transport.price,
                transport=transport.name,
                username=address.username,
                phone=address.phone,
                address=address_info,

            )
        except:
            return JsonResponse(json_msg(8,"创建订单基本数据失败"))
        # 操作订单商品表
        # 操作redis
        r = get_redis_connection()
        cart_key = get_cart_key(user_id)
        goods_total_price = 0
        for sku_id in sku_ids:
            try:
                goods_sku = GoodsSKU.objects.get(pk=sku_id, is_delete=False, is_on_sale=True)
            except GoodsSKU.DoesNotExist:
                # 回滚数据
                transaction.savepoint_rollback(sid)
                return JsonResponse(json_msg(5, "商品不存在"))

            # 获取购物车中商品的数量
            # redis 是基于内存的存储，有可能数据会丢失
            try:
                count = r.hget(cart_key, sku_id)
                count = int(count)
            except:
                transaction.savepoint_rollback(sid)
                return JsonResponse(json_msg(6, "购物车数量不存在"))
            # 判断库存 是否足够
            if goods_sku.stock < count:
                transaction.savepoint_rollback(sid)
                return JsonResponse(json_msg(7, "库存不足"))

            order_goods = OrderGoods.objects.create(
                order=order,
                goods_sku=goods_sku,
                price=goods_sku.price,
                count=count,
            )

            goods_total_price += count * goods_sku.price

            # 扣除库存 销量增加
            goods_sku.stock -= count
            goods_sku.sale_num += count
            goods_sku.save()

        # 再次操作订单基本信息表 商品总金额 订单总金额
        try:
            order_total_price = goods_total_price + transport.price
            order.goods_total_price = goods_total_price
            order.order_total_price = order_total_price
            order.save()
        except:
            # 回滚
            transaction.savepoint_rollback(sid)
            return JsonResponse(json_msg(9,"更新订单失败"))

        # 清空redis中的购物车数据(对应sku_id的)
        r.hdel(cart_key, *sku_ids)


        # 下单成功，提交事务
        transaction.savepoint_commit(sid)
        # 3. 合成响应
        return JsonResponse(json_msg(0, "创建订单成功",data=order_sn))



        # return render(request, 'order/tureorder.html')


class ShowOrder(VerifyLoginView):
    """确认支付页面"""

    def get(self, request):
        return render(request, 'order/order.html')
