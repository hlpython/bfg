from django.shortcuts import render
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from .models import *
from .functions import *
from django.http import JsonResponse
from order.models import *
from django.core.paginator import Paginator
# Create your views here.

def login(request):
    """登录页"""

    return render(request, 'users/login.html', locals())

def register(request):
    """注册页"""
    mess = get_messages(request)
    return render(request, 'users/register.html', locals())

@check_permission
def index(request):
    """用户中心首页"""
    user = User.objects.user_by_name(get_session(request, 'username'))
    # print('user_name',user.user_name)
    return render(request, 'users/user_center_info.html', locals())

@check_permission
def order(request):
    """订单中心首页"""
    # 创建订单中心数据
    # 创建订单基本信息数据对象
    orders = Order.objects.filter(order_user_id=get_session(request, 'uid'))

    # (创建分页器对象)分页显示
    paginator = Paginator(orders, 2)
    # 获取当前分页
    current_page = get(request, 'page')
    if not current_page:
        current_page = 1
    orders = paginator.page(current_page)
    for order in orders:
        order.total = 0
        for goods in order.goodsdetail_set.all():
            order.total += goods.detail_amount * goods.detail_price

    return render(request, 'users/user_center_order.html', locals())

@check_permission
def site(request):
    """收货地址信息页"""
    user = User.objects.user_by_name(get_session(request, 'username'))
    return render(request, 'users/user_center_site.html', locals())

# -------------start----------
# 创建好模型类，接下来从注册开始下手。如何下手？先去看看页面源码。
# 前端客户传过来的数据永远不可信，前端做的简单js验证，只要跟数据库有关我们后端必须对传来的数据进行验证
# 后端验证，怎么验证？这就涉及到前端是通过何种方式把数据传过来的，但是不管是哪种方式，数据验证/处理视图函数肯定是有的
def register_handle(request):
    # 发送来了数据，需要先进行验证
    if check_register_data(request):
        # 用户信息入库
        User.objects.register_data_2_db(request)
        return redirect(reverse('users:login'))
    else:
        return redirect(reverse('users:register'))

# 接受来自register-js，中的ajax对用户名的校验函数的请求，需返回JSON数据
def check_register_username(request):
    if user_is_exist(request):
        return JsonResponse({'ret':1})
    else:
        return JsonResponse({'ret':0})
# ---------------------------------register-end--
# login
# 登录信息校验/处理
def login_handle(request):
    # 先进行简单的验证
    if check_login_data(request):
        # 1.记录用户登录状态（写session）
        keep_user_online(request)
        # 2.是否记住用户名（写cokie）
        response = redirect(reverse('users:index'))
        remember_username(request, response)
        return response
    else:
        return redirect(reverse('users:login'))

# 注销处理函数
def logout_handle(request):
    # 这里还有个先保存上一页，放在后面在去做（原因：现在不想去改模板中的图片链接，不改的话，现在加个记录上一页的中间件会记录图片请求的url
    # 这样就会影响我的进度）
    del_session(request)
    return redirect(reverse('goods:index'))

# 接下来处理user_center_site.html页面中的修改地址的功能。
# 因为设计限制，只能在这修改当前用户信息表中的信息
def address_edit(request):
    # 先简单检测一下
    if check_address_edit_params(request):
        print('addrees')
        # 检测通过，更新user表中对应用户的数据
        User.objects.update_user_info(request)
    return redirect(reverse('users:site'))
