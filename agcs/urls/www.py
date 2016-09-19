from __future__ import unicode_literals
from django.conf.urls import url, include
from django.conf import settings
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.contrib.flatpages.views import flatpage
from django.contrib.flatpages.sitemaps import FlatPageSitemap
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView, TemplateView
from django.views.decorators.cache import cache_page
from machina.apps.forum.app import application as forum_app
from contact.views import ContactView
from landing.models import Service
from landing.sitemaps import LandingSitemap
from community.sitemaps import ForumsSitemap, TopicsSitemap

sitemaps = {
    'flatpages': FlatPageSitemap,
    'landing': LandingSitemap,
    'forums': ForumsSitemap,
    'topics': TopicsSitemap,
}

handler404 = 'agcs.views.page_not_found_view'

urlpatterns = [

    url(r'^$',
        cache_page(60*5)(flatpage),
        {'url': '/'},
        name='home'
    ),

    url(r'^about/$',
        cache_page(60*5)(flatpage),
        {'url': '/about/'},
        name='about'
    ),

    url(r'^contact/$',
        ContactView.as_view(
            success_url='/contact/',
            model=Service,
        ), name='contact'
    ),

    url(r'^community/$',
        forum_app.index_view.as_view(),
        name='community'
    ),

    url(r'^sitemap\.xml$',
        cache_page(60*60)(sitemap),
        {'sitemaps': sitemaps}
    ),

    url(r'^manifest\.json$', cache_page(60*60)(
        TemplateView.as_view(
            content_type='application/json',
            template_name='manifest.json'
        )), {'prefix': getattr(settings, 'FAVICON_PREFIX', None)},
        name='chrome_manifest'
    ),

    url(r'^(home|index)/?$',
        RedirectView.as_view(
            url='/',
            permanent=False
        ), name='redirect-index'
    ),

    url(r'^(?P<name>(home|index|about|contact|services|community))\.html$',
        RedirectView.as_view(
            url='/%(name)s/',
            permanent=True
        ), name='redirect-html'
    ),

    url(r'^favicon\.ico$',
        RedirectView.as_view(
            url=staticfiles_storage.url('img/favicon.ico'),
            permanent=False
        ),
        name='favicon'
    ),

    url(r'^admin/doc/',
        include('django.contrib.admindocs.urls')
    ),

    url(r'^admin/',
        admin.site.urls
    ),

    url(r'^community/',
        include('community.urls')
    ),

    url(r'^',
        include('landing.urls')
    ),
]
