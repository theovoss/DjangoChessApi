from django import template


register = template.Library()


@register.filter
def index(indexable, indx):
    i = int(indx)
    if i < len(indexable):
        return indexable[int(i)]
    return None
