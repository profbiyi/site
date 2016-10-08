from django.utils.deprecation import MiddlewareMixin
from django.utils.cache import patch_vary_headers
from django import get_version
from django.conf import settings
from .utils.functional import set_headers


class VaryAcceptEncodingMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        newheaders = response.has_header('Vary') and (
            response['Vary'].replace(
                ' ', str()
            ).split(',')
        ) or []
        newheaders.append('Accept-Encoding')
        patch_vary_headers(response, list(set(newheaders)))
        return response


class ViaHeaderMiddleware(MiddlewareMixin):
    via_proxies = []

    @property
    def proxies(self):
        return ', '.join(
            self.via_proxies or [
                '%s Django' % get_version()
            ] + getattr(settings, 'VIA_PROXIES', [])
        )

    def process_response(self, request, response):
        set_headers(response, default=True, Via=self.proxies)
        return response
