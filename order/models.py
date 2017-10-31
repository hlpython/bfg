from django.db import models
from db.BaseModel import *


# Create your models here.
class GoodsDetail(BaseModel):
    """订单商品详情信息表"""
    # 商品名称
    detail_name = models.CharField(max_length=50)
    # 商品价格
    detail_price = models.IntegerField()
    # 商品数量
    detail_amount = models.IntegerField()
    # 商品单位
    detail_unit = models.CharField(max_length=100)
    # 商品图片
    detail_img = models.ImageField()
    # 商品ID
    detail_goodsid = models.IntegerField()
    # 订单商品列表
    detail_goods = models.ForeignKey('Order')

class Order(BaseModel):
    """订单基本信息模型"""
    status = (
        (1, '待付款'),
        (2, '待发货'),
        (3, '待收货'),
        (4, '已完成'),
    )

    pay = (
        (1, '货到付款'),
        (2, '微信支付'),
        (3, '支付宝支付'),
        (4, '银联支付'),
    )

    # 订单编号
    order_number = models.CharField(max_length=50)
    # 收货地址
    order_addr = models.CharField(max_length=100)
    # 收货人
    order_recv = models.CharField(max_length=10)
    # 运费
    order_fee = models.IntegerField(default=10)
    # 订单状态
    order_status = models.SmallIntegerField(choices=status, default=1)
    # 支付方式
    order_pay = models.SmallIntegerField(choices=pay, default=1)
    # 订单所属用户
    order_user = models.ForeignKey('users.User')



