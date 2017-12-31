from urllib.parse import urlencode
from django import template

register = template.Library()

@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):
    query = context['request'].GET.dict()

    for (arg,value) in kwargs.items():
        if value is None and arg in query:
            del query[arg]
        else:
            query[arg] = value

    return urlencode(query)
