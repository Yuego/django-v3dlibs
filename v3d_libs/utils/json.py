# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.core.serializers.json import DjangoJSONEncoder
from django.forms.models import ModelChoiceIterator
from django.utils.encoding import force_text

__all__ = ['LazyJSONEncoder']


class LazyJSONEncoder(DjangoJSONEncoder):

    def default(self, o):
        from django.utils.functional import Promise

        if isinstance(o, Promise):
            return force_text(o)
        elif isinstance(o, ModelChoiceIterator):
            return list(o)
        return super(LazyJSONEncoder, self).default(o)
