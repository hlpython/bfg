from django.shortcuts import render
from .models import *
from utils.tool_fun import *
from .functions import *
from django.core.paginator import Paginator

# Create your views here.

@get_total_cart_num
def index(request):
    """商品首页"""
    # 获得广告栏的图片信息
    ads1 = Advertise.objects.all()[:4]
    ads2 = Advertise.objects.all()[4:]
    # 获得所有商品分类信息、
    cags = Category.objects.all()
    # 给每个类分配产品信息
    for cag in cags:
        # 获得最新
        new_goods = GoodsInfo.objects.get_new_goods(cag)
        # 获得最热
        hot_goods = GoodsInfo.objects.get_hot_goods(cag)
        # 分别给上面两个变量的属性归并到cag对象的属性中（为了方便在模板中的召唤）
        cag.new = new_goods
        cag.hot = hot_goods
    return render(request, 'goods/index.html', locals())

@get_total_cart_num
def detail(request):
    """商品详情页"""
    # 获得通过url传参获得的对应商品id而从数据库中查取对应一整条商品信息
    goods = GoodsInfo.objects.get(pk=get(request, 'id'))
    # 获得最新商品
    goods_new = GoodsInfo.objects.get_new_by_all_goods()
    # 关于用户浏览商品记录
    update_user_browse_record(request)
    return render(request, 'goods/detail.html', locals())

@get_total_cart_num
def list(request, cag_id, page_id):
    """商品列表页"""
    # 获取所有商品的类名
    cags = Category.objects.all()
    # 获取重前断传过来的数据
    show = get(request, 'show')

    # 根据商品的分类取出对应的商品列表(在自定义管理器类中定义)
    goods_list = GoodsInfo.objects.get_goods_by_cagid(cag_id, show)
    # 读取新品推荐( 所有)
    goods_new = GoodsInfo.objects.get_new_by_all_goods()
    # 创建分页器对象
    paginator = Paginator(goods_list, 10)
    # 取出对应页的商品(重点)
    current_page = paginator.page(page_id)

    return render(request, 'goods/list.html', locals())


