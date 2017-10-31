from django.db import models
from db.BaseModel import *
from utils.tool_fun import *

"""
Create your models here.
项目正式开始 201710242122
先分析页面 寻找需要维护的数据，用来建模（这是很重要的一个步骤）
先建个基类模型类（因为其他应用都能用得着的字段属性，比如更新时间，添加时间，）

"""

class UserManager(models.Manager):
    """用户信息自定义管理器类"""
    # 用过用户名查找该对应数据是否在数据库的表中
    def user_by_name(self, username):
        try:
            return self.get(user_name=username)
        except User.DoesNotExist:
            return None

    # 将成功注册的用户信息数据保存到数据库中
    def register_data_2_db(self, request):
        user = self.model()
        user.user_name = post(request, 'user_name')
        user.user_mail = post(request, 'user_mail')
        user.user_pass = password_encrypt(post(request, 'user_pass1'))
        user.save()

    # 将用户中心地址也的数据更新（修改）到userbiao中
    def update_user_info(self, request):
        user = self.user_by_name(get_session(request, 'username'))
        user.user_recv = post(request, 'user_recv')
        user.user_addr = post(request, 'user_addr')
        user.user_mail = post(request, 'user_mail')
        user.user_tele = post(request, 'user_tele')
        user.save()


class User(BaseModel):
    """用户信息模型类"""
    # 用户名
    user_name = models.CharField(max_length=20)
    # 用户密码
    user_pass = models.CharField(max_length=100)
    # 用户密码
    user_mail = models.CharField(max_length=50)
    # 用户地址(收件地址)
    user_addr = models.CharField(max_length=50)
    # 用户手机
    user_tele = models.CharField(max_length=11)
    # 邮政编码
    user_code = models.CharField(max_length=10)
    # 收件人姓名
    user_recv = models.CharField(max_length=20, default='')
    # 创建自定义管理器类
    objects = UserManager()


# 用户浏览商品详情页面的记录，另外创建一个表，记录相关数据
class RecordBrowse(BaseModel):

    # 浏览商品详情页面
    browse_goods = models.ForeignKey('goods.GoodsInfo')
    # 浏览者
    browse_user = models.ForeignKey('User')
