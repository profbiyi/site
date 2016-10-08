from django.utils.deprecation import MiddlewareMixin
from django import get_version
from django.conf import settings
from .utils.functional import set_headers


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
