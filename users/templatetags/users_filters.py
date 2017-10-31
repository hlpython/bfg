
from django.template import Library
from django.core.urlresolvers import reverse

register = Library()


# def create_menu(flag):
#     print('000000000000000')
#     menu = [
#         {'link': reverse('users:index'), 'name': '个人信息', 'active': flag == 'info' and 'active' or ''},
#         {'link': reverse('users:order'), 'name': '全部订单', 'active': flag == 'order' and 'active' or ''},
#         {'link': reverse('users:address'), 'name': '收货地址', 'active': flag == 'address' and 'active' or ''},
#     ]
#     # print(menu)
#     return menu
#

# 写一个过滤器，关于用户中心主页面中的最近浏览商品的展示
def browse_sort(goods_list):
    # print('llllceshi',type(goods_list))
    my_goods = list()
    for goods in goods_list:
        my_goods.append(goods)

    my_goods.sort(key=lambda obj:obj.update_time, reverse=True)
    return my_goods


# register.filter('create_menu', create_menu)
register.filter('browse_sort', browse_sort)
