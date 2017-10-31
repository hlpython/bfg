from django.db import models
from utils.common import *
from carts.models import *
from users.models import *

# 定义一个装饰器，用来获取商品的总数量
def get_total_cart_num(view_func):
    def wrapper(request, *args, **kwargs):
        total = 0
        if user_is_login(request):
            carts = Cart.objects.filter(cart_user_id=get_session(request, 'uid'))
            for cart in carts:
                total += cart.cart_amount
        request.total = total
        return view_func(request, *args, **kwargs)
    return wrapper


def update_user_browse_record(request):

    # 只写5条，需先判断用户的登录状态，如果用户已经登录了则不记录
    if not user_is_login(request):
        return

    # 设置最大存储条数
    limit = 5
    goods_id = get(request, 'id')
    user_id = get_session(request, 'uid')
    try:
        record = RecordBrowse.objects.get(browse_goods_id=goods_id, browse_user_id=user_id)
        record.save()
    except RecordBrowse.DoesNotExist:
        # print('ceshi....')
        # 浏览信息不存在则取出所有表中的数据（与该用户相关的）
        records = RecordBrowse.objects.filter(browse_user_id=user_id).order_by('update_time')
        # 先查一下用户数据是否达到5条，没有达到则插入，达到了则修改最早插入的一条数据
        if len(records) < limit:
            # 创建新数据
            r = RecordBrowse()
            r.browse_goods_id = goods_id
            r.browse_user_id = user_id
            r.save()
        else:
            r = records[0]
            r.browse_goods_id = goods_id
            r.save()