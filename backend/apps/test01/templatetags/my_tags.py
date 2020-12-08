from django import template

register = template.Library()


# 过滤器只能传递两个参数|前为第一个
# 可以放在if条件判断中
@register.filter
def multi_filter(x, y):
    return x * y


@register.simple_tag
def multi_tag(x, y):
    return x * y
