from django.db import models

# Create your models here.
from db.base_model import BaseModel


class Transport(BaseModel):
    """运输方式"""
    name = models.CharField(max_length=50, verbose_name="运输方式")
    price = models.DecimalField(max_digits=9, decimal_places=2, default=0, verbose_name='运费')

    def __str__(self):
        return self.name

    class Meta:
        db_table = "transport"
        verbose_name = "运输方式管理"
        verbose_name_plural = verbose_name

        """
        订单表：（下单时的信息备份）
            用户id , 订单编号 , 订单商品金额 , 运费 , 运输方式 , 发货时间 ,收货人姓名 ,收货人电话, 收货地址 , 订单总金额, 
            订单状态（未支付，已支付，已收货，已评价，取消订单，退换货） 支付方式
            
        订单商品表：
            订单表id,商品_sku_id,商品价格,商品数量,,
        """


class Order(BaseModel):
    """订单基本信息表"""
    order_status_choices = (
        (0, '未支付'),
        (1, '已支付'),
        (2, '已发货'),
        (3, '已收货'),
        (4, '未评价'),
        (4, '已完成'),
        (5, '退换货'),
        (6, '取消订单'),
    )

    user = models.ForeignKey(to='user.SpUser', verbose_name='用户', on_delete=models.CASCADE)
    order_sn = models.CharField(max_length=64, verbose_name='订单编号')
    goods_total_price = models.DecimalField(max_digits=9, decimal_places=2, default=0, verbose_name='商品总金额')
    transport_price = models.DecimalField(max_digits=9, decimal_places=2, default=0, verbose_name='运费')
    transport = models.CharField(max_length=50, verbose_name='运输方式')
    username = models.CharField(max_length=50, verbose_name='收货人姓名')
    phone = models.CharField(max_length=11, verbose_name='收货人电话')
    address = models.CharField(max_length=254, verbose_name='收货人地址')
    order_total_price = models.DecimalField(max_digits=9, decimal_places=2, default=0, verbose_name='订单总金额')
    order_status = models.SmallIntegerField(choices=order_status_choices, default=0, verbose_name="订单状态")
    payment = models.ForeignKey(to='Payment', verbose_name="支付方式", null=True, blank=True, on_delete=models.DO_NOTHING)
    pay_time = models.DateTimeField(verbose_name="支付时间", null=True, blank=True)
    deliver_time = models.DateTimeField(verbose_name="发货时间", null=True, blank=True)
    finish_time = models.DateTimeField(verbose_name="完成时间", null=True, blank=True)

    def __str__(self):
        return self.order_sn

    class Meta:
        db_table = "Order"
        verbose_name = "订单管理"
        verbose_name_plural = verbose_name


class OrderGoods(BaseModel):
    """订单商品信息表"""
    order = models.ForeignKey(to="Order", verbose_name="订单ID", on_delete=models.CASCADE)
    goods_sku = models.ForeignKey(to='goods.GoodsSKU', verbose_name="订单商品SKU", on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='商品价格')
    count = models.IntegerField(verbose_name='订单商品数量')

    def __str__(self):
        return "{}{}".format(self.order.order_sn, self.goods_sku.sku_name)

    class Meta:
        db_table = "OrderGoods"
        verbose_name = "订单商品管理"
        verbose_name_plural = verbose_name


class Payment(BaseModel):
    name = models.CharField(max_length=50, verbose_name='支付方式')
    brief = models.CharField(max_length=200, verbose_name='说明', null=True)
    logo = models.ImageField(upload_to="payment", verbose_name='支付LOGO')

    def __str__(self):
        return self.name

    class Meta:
        db_table = "Payment"
        verbose_name = "支付方式管理"
        verbose_name_plural = verbose_name
