from django.db import models
from django.contrib import messages
import hashlib
from django.shortcuts import redirect
from django.core.urlresolvers import reverse

"""
这个模块是用来封装，django基本功能函数
"""

# get
def get(request, key):
    return request.GET.get(key, '').strip()  # strip()的功能是取出字符串首尾两段的所有空格

# post
def post(request, key):
    return request.POST.get(key, '').strip()

def post_list(request, key):
    return request.POST.getlist(key)

# 获取COOKIE
def get_cookie(request, key):
    return request.COOKIES.get(key, '')

# 设置COOKIE
def set_cookie(response, key, value):
    response.set_cookie(key, value, max_age=60*60*24)  # 设置了有效时间为一天

# 删除COOKIE
def del_cookie(response, key):
    response.delete_cookie(key)

# 获取session
def get_session(request, key):
    return request.session.get(key, '')

# 设置session
def set_session(request, key, value):
    request.session[key] = value

# 设置session 过期时间
def set_session_expriry(request, extime):
    request.session.set_expiry(extime)

# 删除session
def del_session(request):
    request.session.flush()

# 关于messages框架（功能携带信息）
# 添加消息
def add_message(request, key, value):
    messages.add_message(request, messages.INFO, key + ':' + value)

# 获取消息
def get_messages(request):
    # 取出messages存储类中的所有消息
    mess = messages.get_messages(request)
    # 遍历取出包含键值对的字符串
    info = dict()
    for message in mess:
        # 这里的message是一个对象
        info_list = str(message).split(':')
        info[info_list[0]] = info_list[1]
    return info

# 入库前给密码加密，不要使用明文，这是不允许的。
def password_encrypt(password, solt=''):
    # 要加密就涉及到使用那种加密方式，MD5安全性没有shaX 好，sha1 被破解过，sha2又有好几种版本，
    # SHA-256可以生成256bit的信息摘要，sha244是sha256的阉割版，sha512可以生成512bit的信息摘要，sha384是sha512的阉割版。
    # 使用哪种加密方式需要权衡安全，性能，空间等因素。根据本项目的需求选择了SHA256来给密码加密，顺便提供加盐的插口
    # 先创建sha256加密对象
    sha = hashlib.sha256()
    # 加盐
    new_password = 'wang' + password + solt + 'wang'
    sha.update(new_password.encode('utf-8'))
    return sha.hexdigest()


# 检测用户是否登录
def check_user_login(request):
    return get_session(request, 'username')

# 在这里写个用户权限装饰器
def check_permission(view_fun):
    def wrapper(request, *args, **kwargs):
        if check_user_login(request):
            return view_fun(request, *args, **kwargs)
        else:
            return redirect(reverse('users:login'))
    return wrapper

