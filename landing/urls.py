from __future__ import unicode_literals
from django.conf.urls import url
from landing.views import ServicesView

urlpatterns = [
    url(r'^services/$',
        ServicesView.as_view(),
        name='services'
    ),
]
