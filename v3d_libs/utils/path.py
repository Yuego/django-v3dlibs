#coding: utf-8
from __future__ import unicode_literals, absolute_import

import os
import re

from django.conf import settings

_clean_uuid_re = re.compile('[^a-z0-9]*', re.I | re.U)


def shard(uuid, length=2, depth=2):
    clean_uuid = _clean_uuid_re.sub('', uuid.lower())

    for i in xrange(depth):
        yield clean_uuid[(length * i):(length * (i + 1))]

    yield uuid


def _get_path_base(instance, prefix='', suffix='', sharding=(2, 2)):
    uuid = instance.get_uuid()
    app = instance._meta.app_label.lower()
    cls = instance.__class__.__name__.lower()

    return os.path.join(prefix, app, cls, suffix, *list(shard(uuid, *sharding)))


def _get_private_path(instance, suffix='', sharding=(2, 2)):
    return _get_path_base(instance, settings.PRIVATE_MEDIA_DIR, suffix=suffix, sharding=sharding)


def _get_public_path(instance, suffix='', sharding=(2, 2)):
    return _get_path_base(instance, settings.PUBLIC_MEDIA_DIR, suffix=suffix, sharding=sharding)


def _get_path(instance, suffix='', sharding=(2, 2), public=True):
    if public:
        return _get_public_path(instance, suffix=suffix, sharding=sharding)
    else:
        return _get_private_path(instance, suffix=suffix, sharding=sharding)


def _get_file_path(instance, filename, suffix='', sharding=(2, 2), public=True):
    dir_name, file_name = os.path.split(filename)
    file_root, file_ext = os.path.splitext(file_name)

    base = _get_path(instance, suffix=suffix, sharding=sharding, public=public)
    return base + file_ext


def gen_file_path(suffix, sharding=(2, 3), public=True):
    return lambda instance, filename: _get_file_path(instance=instance,
                                                     filename=filename,
                                                     suffix=suffix,
                                                     sharding=sharding,
                                                     public=public)


def gen_type_file_path(suffix, extension, sharding=(2, 3), public=True):
    fn = 'somefile.' + extension.strip('.')
    return lambda instance, filename: _get_file_path(instance=instance,
                                                     filename=fn,
                                                     suffix=suffix,
                                                     sharding=sharding,
                                                     public=public)


def gen_dir_path(suffix, sharding=(2, 3), public=True):
    return lambda instance: _get_path(instance=instance,
                                      suffix=suffix,
                                      sharding=sharding,
                                      public=public)
