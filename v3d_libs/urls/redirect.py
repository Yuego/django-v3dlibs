# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.conf.urls import patterns, include, url

from v3d_libs.views.redirect import RedirectToExternalSite

urlpatterns = patterns('',
   url(r'^(?P<url>.*)/$', RedirectToExternalSite.as_view(), name="redirect"),
)

