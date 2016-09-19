import json
from django.views.generic.base import ContextMixin
from django.views.generic.list import ListView
from django.views.decorators.cache import cache_page
from django.contrib import messages
from django.conf import settings
from .mixins import CacheMixin
from .models import Service


class AutoTitleMixin(ContextMixin):
    page_title = None

    @property
    def title(self):
        return (self.page_title or
            self.template_name
                .rpartition('/')[-1]
                .rpartition('.')[0]
                .replace('_', ' ')
        )

    @property
    def common_context(self):
        return {'title' : getattr(self, 'title', None),}

    def get_context_data(self, **kwargs):
        kwargs.update(self.common_context)
        return super(AutoTitleMixin, self).get_context_data(**kwargs)


class LandingPageView(CacheMixin, AutoTitleMixin, ListView):
    cache_timeout = settings.DEBUG and 5 or 3600
    model = Service

class ServicesView(LandingPageView):
    template_name = 'landing/pages/services.html'
