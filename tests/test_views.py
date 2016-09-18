import logging
import importlib
from pathlib import Path
from django.test import TestCase, override_settings
from django.http import Http404
from django.core.urlresolvers import reverse
from django.template.loader import render_to_string
from machina.test.factories import create_forum
from machina.test.factories import create_topic
from machina.test.factories import PostFactory
from machina.test.factories import UserFactory
from agcs.urls import handler404
from agcs.sitemaps import StaticSitemap, ForumsSitemap, TopicsSitemap
from contact.forms import ContactForm
from landing.urls import urlpatterns as landing_urls


class LandingViewsTest(TestCase):

    fixtures = ['services.json']

    def setUp(self):
        self.u1 = UserFactory.create()
        self.top_level_forum = create_forum()
        self.topic = create_topic(forum=self.top_level_forum, poster=self.u1)
        self.post = PostFactory.create(topic=self.topic, poster=self.u1)
        self.topic_pk = self.topic.pk

    def assertStatusOK(self, url):
        self.assertEqual(200,
            self.client.get(url,
                follow=True
            ).status_code,
            msg='url: %s' % url
        )


    def test_get_landing_pages(self):
        for url in landing_urls:
            self.assertStatusOK(reverse(url.name))

    def test_get_manifest(self):
        self.assertStatusOK(reverse('chrome_manifest'))

    def test_get_site_map(self):
        self.assertStatusOK('/sitemap.xml')

    def test_urls_from_site_map(self):
        fsm = ForumsSitemap()
        tsm = TopicsSitemap()
        ssm = StaticSitemap()

        self.assertGreaterEqual(len(fsm.items()), 1)
        self.assertGreaterEqual(len(tsm.items()), 1)
        self.assertGreaterEqual(len(ssm.items()), 1)


class TemplateTagsTest(TestCase):

    def test_landing_utils(self):

        with self.assertRaises(RuntimeError):
            render_to_string('test/landing_utils.html',
                context={
                    'form': ContactForm(),
                    'badpath': 'js/none.js'
                })

        with self.assertRaises(RuntimeError):
            render_to_string('test/landing_utils.html',
                context={
                    'form': ContactForm(),
                    'somedir': 'js'
                })

        render_to_string(
            'test/landing_utils.html',
            context={'form': ContactForm()}
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
