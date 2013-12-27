#coding: utf-8
from __future__ import unicode_literals, absolute_import

from .images import ResizedImageField

try:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], ["^v3d_libs\.fields"])
except ImportError:
    pass
