#coding: utf-8
from __future__ import unicode_literals, absolute_import

from .files import ZipFileField
from .images import ResizedImageField
from .phones import PhonesField

try:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], ["^v3d_libs\.fields"])
except ImportError:
    pass
