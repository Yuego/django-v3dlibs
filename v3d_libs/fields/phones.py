#coding: utf-8
from __future__ import unicode_literals, absolute_import

#import six

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

#from hstore_editor.fields import DictionaryField
from django_hstore.hstore import DictionaryField

import phonenumbers as p
from phonenumbers import NumberParseException

__all__ = ['PhonesField']


class PhonesField(DictionaryField):
    phone_format = p.PhoneNumberFormat.NATIONAL

    """
    def __init__(self, *args, **kwargs):
        _widget_attrs = {
            'key_label': _('telephone'),
            'value_label': _('note'),
            'add_label': _('add telephone'),
            'del_label': _('delete telephone'),
        }
        kwargs.update(_widget_attrs)
        super(PhonesField, self).__init__(*args, **kwargs)
    """
    def clean(self, value, model_instance):
        value = super(PhonesField, self).clean(value, model_instance)

        wrong_numbers = []
        new_numbers = dict()
        for k, v in value.copy().items():
            try:
                phone = p.parse(k, 'RU')
            except NumberParseException:
                wrong_numbers.append(k)
            else:
                new_numbers[p.format_number(phone, self.phone_format)] = v.strip() if v is not None else ''

        if wrong_numbers:
            raise ValidationError(_('Not valid numbers: ') + ', '.join(wrong_numbers))

        return new_numbers

    #def south_field_triple(self):
    #    from south.modelsinspector import introspector
    #    args, kwargs = introspector(self)
    #    return (six.binary_type('v3d_libs.fields.PhonesField'), args, kwargs)
