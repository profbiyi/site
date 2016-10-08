from __future__ import unicode_literals
from django.conf.urls import url
from .views import my_ip_address

urlpatterns = [
    url(r'^', my_ip_address, name='myip'),
]
