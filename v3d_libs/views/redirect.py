# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import
import base64

from django.http import HttpResponseBadRequest
from django.views.generic import RedirectView


class RedirectToExternalSite(RedirectView):
    permanent = True

    def get_redirect_url(self, **kwargs):
        if not 'url' in self.kwargs:
            return HttpResponseBadRequest('Empty redirect url')

        url = self.kwargs.get('url', '')

        #url = urllib.unquote(self.kwargs['url'])
        try:
            decoded_url = base64.urlsafe_b64decode(str(url))
        except UnicodeDecodeError:
            decoded_url = ''

        if not decoded_url:
            decoded_url = self.request.META.get('HTTP_REFERER', '/')

        return decoded_url
