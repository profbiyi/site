from __future__ import unicode_literals
from django.conf.urls import url
from landing.views import (
    ContactView, HomeView,
    AboutView, ServicesView,
    manifest_view
)


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

    url(r'^manifest\.json$',
        manifest_view,
        name='chrome_manifest'
    ),
]
