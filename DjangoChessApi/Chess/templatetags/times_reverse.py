from django import template


register = template.Library()


@register.filter
def times_reverse(max):
    return "".join([str(x) for x in range(int(max) - 1, -1, -1)])
