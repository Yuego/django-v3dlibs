#coding: utf-8
from __future__ import unicode_literals, absolute_import

from django.template import Library

register = Library()

@register.filter
def get_range0(value):
    return range(value)

@register.filter
def get_range1(value):
    return range(1, value + 1)
