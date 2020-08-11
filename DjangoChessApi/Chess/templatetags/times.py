from django import template
register = template.Library()


@register.filter
def times(max):
    return "".join([str(x) for x in range(int(max))])
