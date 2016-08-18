from django.contrib.admin.sites import *
from django.utils.translation import ugettext_lazy

class AdminSite(AdminSite):
    site_title = ugettext_lazy('Alpha Geek Computer Services site admin')
    site_header = ugettext_lazy('AGCS administration')
    index_title = ugettext_lazy('Alpha Geeks administration')

    def get_urls(self):
        from django.conf.urls import url
        urls = super(AdminSite, self).get_urls()
        #urls += [url(r'^my_view/$', self.admin_view(some_view))]
        return urls

site = AdminSite(name='admin')
