from django import template


register = template.Library()


@register.filter
def times(stop):
    return "".join([str(x) for x in range(int(stop))])
