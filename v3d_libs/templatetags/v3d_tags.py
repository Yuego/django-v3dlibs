#coding: utf-8
from __future__ import unicode_literals, absolute_import

from django import template
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


class PaginateNode(template.Node):

    def __init__(self, parser, token):
        bits = token.split_contents()

        if len(bits) > 1:
            raise template.TemplateSyntaxError("%r тег не требует аргументов" % bits[0])

    def render(self, context):
        pages = {}
        if 'page_obj' not in context:
            raise template.TemplateSyntaxError("Контекст не содержит page_obj")

        _page = context['page_obj']
        _paginator = _page.paginator

        _current_number = _page.number
        _first_number = 1
        _last_number = _paginator.num_pages

        if _current_number - _first_number > 4:
            pages.update({'first': 1})

            prev_range = range(_current_number - 4, _current_number)
        elif _current_number == _first_number:
            prev_range = []
        else:
            prev_range = range(1, _current_number)

        if _last_number - _current_number > 4:
            pages.update({'last': _last_number})

            next_range = range(_current_number + 1, _current_number + 5)
        elif _current_number == _last_number:
            next_range = []
        else:
            next_range = range(_current_number + 1, _last_number + 1)

        pages.update({
            'current': _current_number,
            'prev': prev_range,
            'next': next_range,
        })

        context['pages_list'] = pages

        return ''


@register.tag
def paginate(parser, token):
    return PaginateNode(parser, token)
