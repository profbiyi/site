import json
from django.http import JsonResponse
from django.views.generic.base import ContextMixin
from django.views.generic.edit import FormView
from django.views.generic.list import ListView, MultipleObjectMixin
from django.contrib import messages
from django.conf import settings
from django.template.loader import render_to_string
from django.views.decorators.cache import cache_page
from .mixins import CacheMixin, NeverCacheMixin
from .models import Contact, Service
from .forms import ContactForm


class AutoTitleMixin(ContextMixin):
    page_title = None
    pages = [
        'home', 'about', 'contact',
        'community', 'services',
    ]

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
        return {
            self.title : True,
            'pages'    : getattr(self, 'pages', []),
            'title'    : getattr(self, 'title', None),
            'DEBUG'    : getattr(settings, 'DEBUG', False),
            'company'  : getattr(settings, 'COMPANY', None),
            'gapi_key' : getattr(settings, 'GOOGLE_API_KEY', None),
        }

    def get_context_data(self, **kwargs):
        kwargs.update(self.common_context)
        if settings.DEBUG:
            kwargs.update({
                'pages': ['admin:index'] + self.pages
            })
        return super(AutoTitleMixin, self).get_context_data(**kwargs)


class LandingPageView(CacheMixin, AutoTitleMixin,
                        ListView):
    cache_timeout = settings.DEBUG and 5 or 3600
    model = Service


class LandingFormView(NeverCacheMixin, MultipleObjectMixin,
                        AutoTitleMixin, FormView):
    form_class = ContactForm
    model = LandingPageView.model

    @property
    def object_list(self):
        return self.model.objects.all()

    def get_context_data(self, **kwargs):
        kwargs.update(self.common_context)
        if 'form' not in kwargs:
            kwargs['form'] = self.get_form()
        return super(LandingFormView, self).get_context_data(**kwargs)


class HomeView(LandingPageView):
    template_name = 'landing/pages/home.html'


class AboutView(LandingPageView):
    template_name = 'landing/pages/about.html'


class ServicesView(LandingPageView):
    template_name = 'landing/pages/services.html'


class ContactView(LandingFormView):
    template_name = 'landing/pages/contact.html'
    success_url   = '/contact/'
    send_email    = True

    def form_valid(self, form):
        form.instance.remote_address = self.request.META.get('HTTP_X_REAL_IP', '0.0.0.0')
        self.object = form.save()
        self.send_email and form.send_email()
        messages.success(self.request,
            'Thanks! Someone will contact you soon.',
            extra_tags='form_valid',
        )
        return super(ContactView, self).form_valid(form)


@cache_page(settings.DEBUG and 5 or 86400)
def manifest_view(request):
    return JsonResponse(
        json.loads(render_to_string(
            'landing/manifest.json',
            context={'prefix': 'img/favicon/'}
        )), json_dumps_params={'indent': 2}
    )
