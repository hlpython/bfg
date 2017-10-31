from db.BaseModel import *
from django.db import models


# 购物车管理器类
class CartManager(models.Manager):
    pass


# Create your models here.
# 购物车模型
class Cart(BaseModel):
    # 购买的商品
    cart_goods = models.ForeignKey('goods.GoodsInfo')
    # 购买数量
    cart_amount = models.IntegerField()
    # 所属用户
    cart_user = models.ForeignKey('users.User')

    objects = CartManager()