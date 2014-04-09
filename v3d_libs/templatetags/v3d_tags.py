#coding: utf-8
from __future__ import unicode_literals, absolute_import

from django.template import Library
from django.core.urlresolvers import resolve, reverse
from django.utils.translation import activate, get_language

register = Library()

@register.filter
def get_range0(value):
    return range(value)

@register.filter
def get_range1(value):
    return range(1, value + 1)


@register.simple_tag(takes_context=True)
def change_lang(context, lang=None, *args, **kwargs):

    url = context['request'].path
    url_parts = resolve(path=url)
    current_lang = get_language()
    try:
        activate(lang)
        url = reverse(url_parts.view_name, kwargs=url_parts.kwargs)
    finally:
        activate(current_lang)

    return '{0}'.format(url)
