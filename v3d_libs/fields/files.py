#coding: utf-8
from __future__ import unicode_literals, absolute_import

import zlib
from zipfile import ZipFile, BadZipfile, error

from django.db.models import signals, FileField
from django.db.models.fields.files import FileDescriptor
from django.forms import forms

__all__ = ['ZipFileField']


class ZipFileDescriptor(FileDescriptor):
    def __set__(self, instance, value):
        previous_file = instance.__dict__.get(self.field.name)
        super(ZipFileDescriptor, self).__set__(instance, value)

        if previous_file is not None:
            self.field.compute_crc32(instance, force=True)


class ZipFileField(FileField):
    descriptor_class = ZipFileDescriptor

    def __init__(self, verbose_name=None, name=None, upload_to='', storage=None, crc32_field=None, **kwargs):
        self.crc32_field = crc32_field
        super(ZipFileField, self).__init__(verbose_name, name, upload_to, storage, **kwargs)

    def clean(self, value, model_instance):
        data = super(ZipFileField, self).clean(value, model_instance)

        _file = data.file
        try:
            archive = ZipFile(_file, 'r')
            broken = archive.testzip()
        # В случае поврежденного архива BadZipFile иногда не ловится. странную ошибку error тоже поймать не смог
        except Exception:
            raise forms.ValidationError('Файл "%s" не является ZIP-архивом или повреждён' % data.name)
        else:
            if broken is not None:
                raise forms.ValidationError('Архив "%s" повреждён' % data.name)

        return data

    def contribute_to_class(self, cls, name):
        super(ZipFileField, self).contribute_to_class(cls, name)
        # Attach update_dimension_fields so that dimension fields declared
        # after their corresponding image field don't stay cleared by
        # Model.__init__, see bug #11196.
        signals.post_init.connect(self.compute_crc32, sender=cls)

    def compute_archive_crc32(self, archive):
        crc = 0
        for line in archive:
            crc = zlib.crc32(line, crc)
        return '%X' % (crc & 0xFFFFFFFF)

    def compute_crc32(self, instance, force=False, *args, **kwargs):

        # Не указано поле для хранения crc32. Выходим
        if self.crc32_field is None:
            return

        # Поле файла не заполнено и не нужно считать принудительно
        archive = getattr(instance, self.attname)

        if not archive and not force:
            if not archive:
                setattr(instance, self.crc32_field, None)
            return

        # CRC32 уже посчитан и не форсирован пересчет
        if getattr(instance, self.crc32_field) and not force:
            return

        if archive:
            setattr(instance, self.crc32_field, self.compute_archive_crc32(archive))
        else:
            setattr(instance, self.crc32_field, None)
