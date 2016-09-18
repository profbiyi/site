from __future__ import unicode_literals
from django.conf.urls import url, include
from django.conf import settings
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView
from machina.apps.forum.app import application as forum_app
from landing.models import Service
from landing.views import HomeView
from contact.views import ContactView

from .sitemaps import (
    StaticSitemap,
    ForumsSitemap,
    TopicsSitemap
)

sitemaps = {
    'static': StaticSitemap,
    'forums': ForumsSitemap,
    'topics': TopicsSitemap,
}

handler404 = 'agcs.views.page_not_found_view'

_pages = getattr(settings,'LOCAL_CONTEXT', {}).get('pages', [])

urlpatterns = [

    url(r'^',
        include('landing.urls')
    ),

    url(r'^$',
        HomeView.as_view(),
        name='home'
    ),

    url(r'^sitemap\.xml$',
        sitemap,
        {'sitemaps': sitemaps},
        name='django.contrib.sitemaps.views.sitemap'
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

    url(r'^community/$',
        forum_app.index_view.as_view(),
        name='community',
    ),

    url(r'^community/',
        include('community.urls')
    ),

    url(r'^contact/$',
        ContactView.as_view(
            success_url='/contact/',
            model=Service,
        ), name='contact'
    ),

    # url(r'contact/', ContactView.as_view(
    #     object_list=Service.objects.all(),
    #     pages=['home', 'about', 'contact', 'community', 'services',],
    #     template_name='contact/contact.html'
    # ), name='contact'),
]
