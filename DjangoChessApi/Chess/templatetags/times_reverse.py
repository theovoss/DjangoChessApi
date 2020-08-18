from django import template


register = template.Library()


@register.filter
def times_reverse(stop):
    return "".join([str(x) for x in range(int(stop) - 1, -1, -1)])
