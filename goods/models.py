from django.db import models
from db.BaseModel import *
from tinymce.models import HTMLField

# Create your models here.


# 分类模型
class Category(BaseModel):
    # 产品分类名称
    cag_name = models.CharField(max_length=30)


# 商品信息管理类
class GoodsInfoManager(models.Manager):
    # 从数据库中获取最新的商品(4个最新的)
    def get_new_goods(self, cag):
        return self.filter(goods_cag=cag).order_by('-id')[:4]

    # 获得最热的3个商品
    def get_hot_goods(self, cag):
        return self.filter(goods_cag=cag).order_by('-goods_visits')[:3]

    # 获得所有商品中最新的两个商品
    def get_new_by_all_goods(self):
        return self.all().order_by('-id')[:2]


    def get_goods_by_cagid(self, cag_id, show):
        if show == 'price':
            return GoodsInfo.objects.filter(goods_cag_id=cag_id).order_by('-goods_price')
        if show == 'hot':
            return GoodsInfo.objects.filter(goods_cag_id=cag_id).order_by('-goods_visits')
        return self.filter(goods_cag_id=cag_id)


class GoodsInfo(BaseModel):
    # 商品名称
    goods_name = models.CharField(max_length=30)
    # 商品价格
    goods_price = models.IntegerField()
    # 商品的图片
    goods_image = models.ImageField()
    # 商品简述
    goods_short = models.CharField(max_length=100)
    # 商品详情
    goods_desc = HTMLField()
    # 上品上架
    goods_status = models.BooleanField(default=True)
    # 商品单位
    goods_unit = models.CharField(max_length=20)
    # 商品访问量
    goods_visits = models.IntegerField(default=0)
    # 商品销量
    goods_sales = models.IntegerField(default=0)
    # 商品分类
    goods_cag = models.ForeignKey(Category)
    # 自定义管理器类
    objects = GoodsInfoManager()


# 广告模型
class Advertise(BaseModel):
    # 广告名字
    ad_name = models.CharField(max_length=30)
    # 广告图片
    ad_image = models.ImageField(upload_to='ad')
    # 广告链接
    ad_link = models.CharField(max_length=100)
