from django import template
register = template.Library()

@register.filter
def index(indexable, index):
    i = int(index)
    if(i < len(indexable)):
        return indexable[int(i)]
