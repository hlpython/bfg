from django.shortcuts import render
from utils.tool_fun import *
from carts.models import *
from users.models import *
from django.http import JsonResponse
from .models import *
import random
import time
from django.db import transaction


# Create your views here.
@check_permission
def index(request):
    """订单中心页"""
    goods_id_list = post_list(request, 'goods_id')

    # 将商品id列表合并成字符串，方便请求时携带（提交表单）
    goods_string = ','.join(goods_id_list)
    # user_id = get_session(request, 'uid')
    # print('goods_id', goods_id_list)
    # print('user_id', user_id)
    # 查询/获取对应用户提交的物品
    carts = Cart.objects.filter(cart_user_id=get_session(request, 'uid'), cart_goods_id__in=goods_id_list)

    total_nums = 0
    total_money = 0
    for cart in carts:
        # 累计商品总数
        total_nums += cart.cart_amount
        # 计算该条商品的单品总价
        cart.single_total_money = cart.cart_goods.goods_price * cart.cart_amount
        # 计算商品总价
        total_money += cart.single_total_money
    # 将商品数量和总价属性绑定到carts对象上去
    carts.total_nums = total_nums
    carts.total_money = total_money
    # 获取用户信息
    user = User.objects.get(id=get_session(request, 'uid'))
    return render(request, 'order/place_order.html', locals())

# 装饰成事务函数（相当于数据库中的事务，可以回滚的，防止误操作）
@transaction.atomic
def order_handle(request):
    """订单页面提交数据处理及页面跳转"""
    goods_ids = post(request, 'goods_list_str').split(',')
    goods_pay = post(request, 'pay_style')
    user_id = get_session(request, 'uid')
    print('goods_ids', goods_ids)
    print('goods_pay', goods_pay)
    print('user_id', user_id)
    # 获取购物车表数据对象
    carts = Cart.objects.filter(cart_user_id=user_id, cart_goods_id__in=goods_ids)
    # print('ccccccccccccccc')
    # 获取用户信息表的数据对象
    user = User.objects.get(id=user_id)
    # 创建事务的还原点(回滚点)
    save_point = transaction.savepoint()
    try:
        # 创建基础订单信息
        order = Order()
        order.order_addr = user.user_addr
        order.order_recv = user.user_recv
        order.order_pay = goods_pay
        order.order_user = user
        order.order_number = str(user_id) + str(int(time.time())) + str(random.randint(1000, 9999))
        order.save()

        # 创建订单商品信息
        for cart in carts:
            deatail = GoodsDetail()
            deatail.detail_name = cart.cart_goods.goods_name
            deatail.detail_goodsid = cart.cart_goods_id
            deatail.detail_price = cart.cart_goods.goods_price
            deatail.detail_amount = cart.cart_amount
            deatail.detail_img = cart.cart_goods.goods_image
            deatail.detail_unit = cart.cart_goods.goods_unit
            deatail.detail_goods = order
            deatail.save()
        # 订单提交成功，立即删除对应购物车的数据
        carts.delete()
        # 成功保存数据到列表，即可提交事物
        transaction.savepoint_commit(save_point)
        return JsonResponse({'ret':1})
    except:
        return JsonResponse({'ret':0})
    # return render(request, 'users/user_center_order.html', locals())