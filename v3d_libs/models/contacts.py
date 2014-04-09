# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _

from v3d_libs.fields import PhonesField

__all__ = ['ContactBase']


class ContactBase(models.Model):
    class Meta:
        abstract = True


    site_url = models.URLField(_('site url'), max_length=255, blank=True)
    email = models.EmailField(_('email'), blank=True)
    phones = PhonesField(_('contact phones'), blank=True, null=True)

    show_contacts = models.BooleanField(_('show contacts'), default=True,
        help_text='Отображать контактную и контактную информацию на сайте')

    @property
    def has_contacts(self):
        return bool(self.show_contacts and (self.site_url or self.email or self.contact_phones))
