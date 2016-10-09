from django.http import HttpResponse
from django.test import TestCase, RequestFactory, modify_settings
from django.utils.decorators import decorator_from_middleware
from headers.middleware import (
    MultipleProxyMiddleware,
    ViaHeaderMiddleware
)


def goodview(request, *args, **kwargs):
    return HttpResponse(
        "Hello world",
        content_type="text/html"
    )


class HeadersMiddleWareTest(TestCase):

    def setUp(self):
        self.rf = RequestFactory()

    def test_with_extra_meta(self):
        req = self.rf.get('/')
        for f in getattr(
            MultipleProxyMiddleware,
            'FORWARDED_FOR_FIELDS'
        ): req.META[f] = 'Value1'
        req.META['HTTP_X_FORWARDED_FOR'] += ',Foo'
        req.META['SERVER_SOFTWARE'] = 'foo/1.1'
        viawrap = decorator_from_middleware(ViaHeaderMiddleware)
        mulwrap = decorator_from_middleware(MultipleProxyMiddleware)
        viawrap(mulwrap(goodview))(req)

    def test_multi_proxy(self):
        with self.modify_settings(MIDDLEWARE_CLASSES={
            'prepend': 'headers.middleware.MultipleProxyMiddleware',
        }):
            req = self.rf.get('/',
                SERVER_NAME='www.alphageek.xyz',
                SERVER_SOFTWARE='server/1.1',
                HTTP_X_FORWARDED_FOR='Foo, Bar'
            )
            res = self.client.get('/', **req.META)
            print(res.serialize_headers().decode())

