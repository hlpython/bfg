from django.db import models
from utils.tool_fun import *
import re
from .models import *

"""
这个模块里用来定义一些与user相关的函数。
"""

def check_register_data(request):
    user_name = post(request, 'user_name')
    user_mail = post(request, 'user_mail')
    user_pass1 = post(request, 'user_pass1')
    user_pass2 = post(request, 'user_pass2')

    flag = True
    if not (5 <= len(user_name) <= 20):
        flag = False
        add_message(request, 'user_name', '用户名不合法！')

    if not (8 <= len(user_pass1) <= 20):
        flag = False
        add_message(request, 'user_pass', '密码不合法！')

    if len(user_pass1) != len(user_pass2):
        flag = False
        add_message(request, 'user_pass', '两次密码不一致！')

    # 判断邮箱是否合法
    reg = '^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(.[a-z]{2,5}){1,2}$'
    if not re.match(reg, user_mail):
        flag = False
        add_message(request, 'user_mail', '输入的邮箱不合法..！')

     # 判断用户名是否存在
    if User.objects.user_by_name(user_name):
        flag = False
        add_message(request, 'user_name', '用户名已存在..！')
    return flag

# 注册页面填写用户名的时候对用户是否存在于数据库系统进行校验
def user_is_exist(request):
    username = get(request, 'username')
    print('username:',username)
    return User.objects.user_by_name(username)
# ------------------------------------

# 用户信息登录处理/校验
def check_login_data(request):
    user_name = post(request, 'user_name')
    user_pass = post(request, 'user_pass')
    # 先进行简单的校验
    if not (5 <= len(user_name) <= 20):
        return False
    if not (8 <= len(user_pass) <= 20):
        return False

    # 再检查数据库中是否存在该用户名
    user = User.objects.user_by_name(user_name)
    if not user:
        return False
    else:
        if user.user_pass == password_encrypt(user_pass):
            return True
        else:
            return False


# 记录用户登录状态（写进session）
def keep_user_online(request):
    user = User.objects.user_by_name(post(request, 'user_name'))
    set_session(request, 'username', user.user_name)
    set_session(request, 'uid', user.id)
    set_session_expriry(request, 60*60*24)


# 登录是对记住用户名选项进行处理(写进cookie)
def remember_username(request, response):
    remember_name = post(request, 'user_memb')
    if remember_name:
        set_cookie(response, 'username', post(request, 'user_name'))


# 关于用户中心的地址编辑页面(数据检测)
def check_address_edit_params(request):
    user_recv = post(request, 'user_recv')
    user_addr = post(request, 'user_addr')
    user_code = post(request, 'user_code')
    user_tele = post(request, 'user_tele')
    # print(user_recv)
    # print(user_addr)
    # print(user_code)
    # print(user_tele)
    # 先进行基础的检测
    if not (5 <= len(user_recv) <= 20 and user_addr and len(user_code) == 6 and len(user_tele) == 11):
        print('111111')
        return False
    return True



