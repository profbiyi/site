from __future__ import unicode_literals
from django.conf.urls import url, include
from django.contrib import admin, admindocs
from django.contrib.sitemaps.views import sitemap
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView
from django_markdown.views import preview
from machina.apps.forum.app import application as forum_app
from community import urls as community_urls

from landing.views import (
    ContactView, HomeView,
    AboutView, ServicesView,
    manifest_view
)

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
#handler500 = 'agcs.views.server_error_view'
#handler403 = 'agcs.views.permission_denied_view'
#handler400 = 'agcs.views.bad_request_view'

urlpatterns = [

    url(r'^services/$',
        ServicesView.as_view(),
        name='services'
    ),

    url(r'^about/$',
        AboutView.as_view(),
        name='about'
    ),

    url(r'^contact/$',
        ContactView.as_view(),
        name='contact'
    ),

    url(r'^(home|index)/$',
        HomeView.as_view(),
        name='home'
    ),

    url(r'^$',
        HomeView.as_view(),
        name='home'
    ),

    url(r'^manifest\.json$',
        manifest_view,
        name='chrome_manifest'
    ),

    url(r'^sitemap\.xml$',
        sitemap,
        {'sitemaps': sitemaps},
        name='django.contrib.sitemaps.views.sitemap'
    ),

    url(r'^favicon\.ico$',
        RedirectView.as_view(
            url=staticfiles_storage.url('assets/img/favicon.ico'),
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

    url(r'^markdown/preview/$',
        preview,
        name='django_markdown_preview',
    ),

    url(r'^community/$',
        forum_app.index_view.as_view(),
        name='community'
    ),

    url(r'^community/',
        include(community_urls)
    ),


]
