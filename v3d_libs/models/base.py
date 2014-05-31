# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _

from django_extensions.db.fields import (UUIDField,
                                         CreationDateTimeField, ModificationDateTimeField)

__all__ = ['BaseInfo']


class BaseInfo(models.Model):

    class Meta:
        abstract = True

    uuid = UUIDField('UUID')
    pub_date = CreationDateTimeField(_('publication date'), editable=True)
    last_modified = ModificationDateTimeField(_('last update'))
    created = CreationDateTimeField(_('created at'))

    def get_uuid(self):
        if self.uuid is None:
            field = self._meta.get_field('uuid')
            return field.pre_save(self, True)

        return self.uuid
