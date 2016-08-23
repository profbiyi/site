from django.test import TestCase, Client


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
