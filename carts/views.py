from django.shortcuts import render
from utils.tool_fun import *
from django.http import JsonResponse
from .models import *

# Create your views here.
@check_permission
def index(request):
    """购物车主页"""
    # 接下来在请求购物车页面数据时，我们需要将相关数据传过去
    # 取出购物车表中的所有商品
    carts = Cart.objects.filter(cart_user_id=get_session(request, 'uid'))
    # 记录总数量
    total = 0
    # 记录总价
    money = 0
    # 记录单品总价
    # single_total = 0
    # 遍历购物车统计上面两个主要参数
    for cart in carts:
        # 计算单品总价
        cart.single_total = cart.cart_amount * cart.cart_goods.goods_price
        # 累计商品总数量
        total += cart.cart_amount
        # 累加商品总价格
        money += cart.single_total

        carts.total = total
        carts.money = money
    return render(request, 'carts/cart.html', locals())

def add_goods(request):
    """在商品详情页面添加商品后端效果"""
    # 1. 获取用户ID、商品ID、商品数量
    goods_id = get(request, 'goods_id')
    user_id = get_session(request, 'uid')
    goods_num = get(request, 'goods_num')
    try:
        # 查看商品是否存在，存在即更新，不存在即添加
        cart = Cart.objects.get(cart_goods_id=goods_id, cart_user_id=user_id)
        cart.cart_amount = cart.cart_amount + int(goods_num)
        # print('ssss')
        cart.save()
    except Cart.DoesNotExist:
        c = Cart()
        c.cart_goods_id = goods_id
        c.cart_user_id = user_id
        c.cart_amount = goods_num
        # print('xxxxx')
        c.save()
    # 使用聚合计算商品的总数量(返回的是一个字典)
    total = Cart.objects.filter(cart_user_id=user_id).aggregate(models.Sum('cart_amount'))['cart_amount__sum']
    print(total)
    return JsonResponse({'total':total})

def remove_goods(request):
    """删除商品处理函数"""
    goods_id = get(request, 'goods_id')
    try:
        # 查寻数据
        goods = Cart.objects.get(cart_goods_id=goods_id, cart_user_id=get_session(request, 'uid'))
        goods.delete()
    except Cart.DoesNotExist:
        print('购物车数据删除失败！\n失败原因：未找到相关数据。')
    return JsonResponse({'ret':1})

def edit_goods_num(request):
    """用户商品数量信息更新"""
    # 获取商品id
    goods_id = get(request, 'goods_id')
    # 获取商品数量
    goods_nums = get(request, 'goods_nums')
    # print('商品id', goods_id)
    # print('数量更新函数测试',goods_id, goods_nums)
    # 更新商品信息
    try:
        goods = Cart.objects.get(cart_user_id=get_session(request, 'uid'), cart_goods_id=goods_id)
        goods.cart_amount = goods_nums
        goods.save()
    except Cart.DoesNotExist:
        return JsonResponse({'ret':0})
    return JsonResponse({'ret':1})
