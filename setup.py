#!/usr/bin/env python
from distutils.core import setup
import sys
sys.path.insert(0, '..')

from v3d_libs.version import __version__

for cmd in ('egg_info', 'develop', 'build_sphinx', 'upload_sphinx'):
    if cmd in sys.argv:
        from setuptools import setup

setup(
    name='v3d_libs',
    version=__version__,
    author='Artem Vlasov',
    author_email='root@proscript.ru',
    url='https://github.com/Yuego/v3d_libs',
    download_url='https://github.com/Yuego/v3d_libs/archive/%s.tar.gz' % __version__,

    description='Something for Django',
    long_description=open('README.rst').read(),

    license='MIT license',
    requires=[
        'django (>=1.3)',
        'pillow',
        'six',
    ],
    packages=[
        'v3d_libs',
        'v3d_libs.fields',
    ],
    classifiers=[
        'Development Status :: 1 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: Russian',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Framework :: Django',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
