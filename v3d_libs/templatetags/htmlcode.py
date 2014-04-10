# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import template
from django.utils.html import escape
from django.utils.safestring import mark_safe

register = template.Library()


class HTMLCodeNode(template.Node):
    def __init__(self, nodelist):
        self.nodelist = nodelist

    def render(self, context):
        content = self.nodelist.render(context)
        return mark_safe(escape(content.strip()).encode('ascii', 'xmlcharrefreplace'))


@register.tag
def htmlcode(parser, token):

    nodelist = parser.parse(('endhtmlcode',))
    parser.delete_first_token()

    return HTMLCodeNode(nodelist)
