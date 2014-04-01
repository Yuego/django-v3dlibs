#coding: utf-8
from __future__ import unicode_literals, absolute_import

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db.models.fields import CharField
from django.utils.translation import ugettext_lazy as _

from django_hstore.hstore import DictionaryField

import phonenumbers as p
from phonenumbers import NumberParseException

__all__ = ['PhoneField', 'PhonesField']

default_format = getattr(settings, 'DEFAULT_PHONE_FORMAT', p.PhoneNumberFormat.NATIONAL)
default_region = getattr(settings, 'DEFAULT_PHONE_REGION', None)

class PhoneField(CharField):

    def __init__(self, *args, **kwargs):
        kwargs.update({
            'max_length': 25,
        })
        self._format = kwargs.pop('phone_format', default_format)
        self._region = kwargs.pop('phone_region', default_region)

        super(PhoneField, self).__init__(*args, **kwargs)

    def clean(self, value, model_instance):
        value = super(PhoneField, self).clean(value, model_instance)

        if value:
            try:
                phone = p.parse(value, self._region)
            except NumberParseException:
                raise ValidationError('Not valid number: {0}'.format(value))
            else:
                value = p.format_number(phone, self._format)

        return value


class PhonesField(DictionaryField):

    def __init__(self, *args, **kwargs):
        self._format = kwargs.pop('phone_format', default_format)
        self._region = kwargs.pop('phone_region', default_region)

        super(PhonesField, self).__init__(*args, **kwargs)

    def clean(self, value, model_instance):
        value = super(PhonesField, self).clean(value, model_instance)

        wrong_numbers = []
        new_numbers = dict()
        for k, v in value.copy().items():
            try:
                phone = p.parse(k, self._region)
            except NumberParseException:
                wrong_numbers.append(k)
            else:
                new_numbers[p.format_number(phone, self._format)] = v.strip() if v is not None else ''

        if wrong_numbers:
            raise ValidationError(_('Not valid numbers: ') + ', '.join(wrong_numbers))

        return new_numbers

    #def south_field_triple(self):
    #    from south.modelsinspector import introspector
    #    args, kwargs = introspector(self)
    #    return (six.binary_type('v3d_libs.fields.PhonesField'), args, kwargs)
