from django import template


register = template.Library()


@register.filter
def inc(value, value2):
    return int(value)*int(value2)


@register.simple_tag
def division(*args, **kwargs):
    if 'to_int' in kwargs:
        return int(int(args[0])/int(args[1]))
    else:
        return float(args[0])/float(args[1])
