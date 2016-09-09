import logging
import importlib
from django.test import TestCase
from django.http import Http404
from agcs.urls import handler404


__all__ = ['LandingViewsTest']


class LandingViewsTest(TestCase):

    def test_get_landing_pages(self):
        for page in [
            '/', '/about/', '/services/',
            '/contact/', '/community/',
        ]:  self.assertEqual(200,
                self.client.get(page,
                    follow=True
                ).status_code
            )

    def test_get_site_maps(self):
        self.assertEqual(200,
            self.client.get('/sitemap.xml',
                follow=True
            ).status_code
        )


class ErrorPageViewsTest(TestCase):

    def setUp(self):
        self.logger = logging.getLogger('django.request')
        self.old_level = self.logger.getEffectiveLevel()
        self.logger.setLevel(logging.ERROR)

    def tearDown(self):
        self.logger.setLevel(self.old_level)

    def test_page_not_found(self):
        module, name = handler404.rsplit('.', 1)
        response = self.client.get('/foo/bar.baz')
        self.assertHTMLEqual(response.content.decode(),
            getattr(importlib.import_module(module), name)(
                response.request, Http404('Bad request')
            ).content.decode()
        )
