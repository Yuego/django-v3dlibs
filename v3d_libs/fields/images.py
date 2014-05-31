#coding: utf-8
from __future__ import unicode_literals, absolute_import

import six
try:
    from PIL import Image, ImageFile
except ImportError:
    import Image
    import ImageFile

from django.conf import settings
from django.core.files.base import ContentFile

from django.db.models import ImageField

DEFAULT_SIZE = getattr(settings, 'V3D_RESIZED_DEFAULT_SIZE', [1024, 768])

__all__ = ['ResizedImageField']


class ResizedImageFieldFile(ImageField.attr_class):

    def save(self, name, content, save=True):
        new_content = six.StringIO()
        content.file.seek(0)
        thumb = Image.open(content.file)

        width, height = thumb.size
        if width > self.field.max_width or height > self.field.max_height:
            thumb.thumbnail((
                self.field.max_width,
                self.field.max_height
                ), Image.ANTIALIAS)

            if self.field.use_thumbnail_aspect_ratio:
                img = Image.new("RGBA", (self.field.max_width, self.field.max_height), self.field.background_color)
                img.paste(thumb, ((self.field.max_width - thumb.size[0]) / 2, (self.field.max_height - thumb.size[1]) / 2))
            else:
                img = thumb

            img_format = self.field.format if self.field.format else thumb.format
            quality = self.field.quality if self.field.quality else 85
            info = img.info.copy()

            if img_format.upper() == 'JPEG':
                info['quality'] = quality

            if self.field.compression:
                info.update({'compression': self.field.compression})

            if 'optimize' in info or 'progressive' in info:
                #HACK: иначе не сохраняет JPEG
                maxblock = ImageFile.MAXBLOCK
                ImageFile.MAXBLOCK = img.size[0] * img.size[1]

                img.save(new_content, format=img_format, **info)

                ImageFile.MAXBLOCK = maxblock
            else:
                img.save(new_content, format=img_format, **info)

            new_content = ContentFile(new_content.getvalue())
        else:
            new_content = content

        super(ResizedImageFieldFile, self).save(name, new_content, save)


class ResizedImageField(ImageField):

    attr_class = ResizedImageFieldFile

    def __init__(self, verbose_name=None, name=None, **kwargs):
        self.max_width = kwargs.pop('max_width', DEFAULT_SIZE[0])
        self.max_height = kwargs.pop('max_height', DEFAULT_SIZE[1])
        self.use_thumbnail_aspect_ratio = kwargs.pop('use_thumbnail_aspect_ratio', False)
        self.background_color = kwargs.pop('background_color', (255, 255, 255, 0))
        self.format = kwargs.pop('format', 'jpeg')
        self.compression = kwargs.pop('compression', 'jpeg')
        self.quality = kwargs.pop('quality', None)
        super(ResizedImageField, self).__init__(verbose_name, name, **kwargs)

