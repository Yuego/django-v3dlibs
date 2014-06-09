# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import template
from django_hosts.reverse import reverse_full

from v3d_libs.utils.http import encode_link

register = template.Library()


class ELinkNode(template.Node):
    def __init__(self, parser, token):

        bits = token.split_contents()

        if len(bits) != 3:
            raise template.TemplateSyntaxError("%r tag requires exactly 3 arguments" % bits[0])

        self.link = parser.compile_filter(bits[1])
        self.title = parser.compile_filter(bits[2])

    def render(self, context):
        link = self.link.resolve(context)
        title = self.title.resolve(context)
        url = reverse_full('redirect', 'redirect', (), {}, (encode_link(link),))

        return '<a href="%s" title="%s" target="_blank" rel="nofollow">%s</a>' % (url, title, title)


@register.tag
def elink(parser, token):
    return ELinkNode(parser, token)

@register.filter
def redirect(link):
    return reverse_full('redirect', 'redirect', (), {}, (encode_link(link),))
