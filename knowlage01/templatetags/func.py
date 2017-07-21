from django import template
register=template.Library()


@register.filter()
def my_func(value):
    pass
