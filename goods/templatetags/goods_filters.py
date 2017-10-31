from django.template import Library

"""
过滤器模块。
"""

# 创建个对象
register = Library()

def create_image_name(index):
    return 'images/banner0' + str(index) + '.jpg'

def convert_str_to_int(page_id):
    return int(page_id)

register.filter('create_image_name', create_image_name)
register.filter('convert_str_to_int', convert_str_to_int)
