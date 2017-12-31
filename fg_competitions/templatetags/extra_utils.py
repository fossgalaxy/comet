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

@register.simple_tag
def dict_contains(**kwargs):
    """given a dictionary, and some object o, return true if o is a key in dictionary"""
    d = kwargs['d']
    n = kwargs['n']
    return n in d.keys()

@register.simple_tag
def dict_get(**kwargs):
    d = kwargs['d']
    n = kwargs['n']
    if n not in d:
        return None
    else:
        return d[n]
