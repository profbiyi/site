from django.contrib import sitemaps
from machina.apps.forum.models import Forum
from community.apps.forum_conversation.models import Post, Topic
from django.core.urlresolvers import reverse

class StaticViewSitemap(sitemaps.Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self):
        return ['home', 'contact', 'about', 'services', 'community']

    def location(self, item):
        return reverse(item)

class ForumSitemap(sitemaps.Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self):
        return Forum.objects.all()

    def lastmod(self, obj):
        return obj.last_post_on

    def location(self, item):
        return '/community/forum/{0}-{1}/'.format(
            item.name.replace(' ','-').replace('/', '').lower(),
            item.pk
        )





