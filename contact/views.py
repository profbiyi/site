from django.views.generic.edit import FormView
from django.views.generic.base import ContextMixin
from django.views.generic.list import MultipleObjectMixin
from django.contrib import messages
from django.conf import settings
from .models import Contact
from .forms import ContactForm

class ContactView(MultipleObjectMixin, FormView):
    template_name = 'contact/contact.html'
    page_title = 'contact'
    success_url = '/contact/'
    form_class = ContactForm

    @property
    def object_list(self):
        return self.get_queryset()

    def get_context_data(self, **kwargs):
        kwargs.update({
            'gapi_key' : getattr(settings, 'GOOGLE_API_KEY', None),
        })
        if 'form' not in kwargs:
            kwargs['form'] = self.get_form()
        return super(ContactView, self).get_context_data(**kwargs)

    def form_valid(self, form):
        form.instance.remote_address = self.request.META.get('HTTP_X_REAL_IP', '0.0.0.0')
        try:
            self.object = form.save()
            form.send_email()
        except: # pragma: no cover
            messages.error(self.request,
                'An internal server error occured.',
                extra_tags='form_invalid',
            )
        else:
            messages.success(self.request,
                'Thanks! Someone will contact you soon.',
                extra_tags='form_valid',
            )
        return super(ContactView, self).form_valid(form)
