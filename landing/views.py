from django.views.generic.base import TemplateView
from django.utils.module_loading import import_string
from django.conf import settings
from .mixins import CacheMixin
from .models import Service


class LandingPageView(CacheMixin, TemplateView):
    cache_timeout = settings.DEBUG and 5 or 300

    def get_context_data(self, **kwargs):
        try:
            has_services = 'landing.core.context_processors.services' in (
                import_string('django.template.engines').templates
                    ['django']['OPTIONS']['context_processors']
            )
        except (KeyError, AttributeError):
            has_services = False

        if not has_services:
            kwargs.update({
                'service_list': Service.objects.all(),
            })

        return super(LandingPageView, self).get_context_data(**kwargs)


class ServicesView(LandingPageView):
    template_name = 'landing/pages/services.html'
