from django import forms
from django.conf import settings
from django.http import HttpResponse
from django.core.mail import EmailMultiAlternatives, BadHeaderError
from django.template.loader import render_to_string
from snowpenguin.django.recaptcha2.fields import ReCaptchaField
from snowpenguin.django.recaptcha2.widgets import ReCaptchaWidget
from .models import Contact


class ContactForm(forms.ModelForm):

    class Meta:
        model = Contact
        fields = [
            'first_name', 'last_name',
            'phone', 'email', 'comment',
        ]

    cc_myself = forms.BooleanField(required=False, initial=False)
    captcha = ReCaptchaField(label="   ", widget=ReCaptchaWidget())

    def send_email(self):

        msg = EmailMultiAlternatives(**{
            'subject'    : 'Contact Form: ' + str(self.instance.name),
            'from_email' : settings.EMAIL_HOST_USER,
            'reply_to'   : [self.cleaned_data['email']],
            'to'         : tuple(i[1] for i in settings.ADMINS) + (
                            self.cleaned_data['cc_myself'] and (
                            self.cleaned_data['email'],) or tuple()),
            'body'       : str().join('{0:15s} : {1}\n'.format(
                            self.fields[f].label, self.cleaned_data[f])
                            for f in self._meta.fields),
        })

        msg.attach_alternative(
            render_to_string(
                'contact/email.html',
                context={
                    'name'    : str(self.instance.name),
                    'phone'   : self.cleaned_data['phone'],
                    'email'   : self.cleaned_data['email'],
                    'comment' : self.cleaned_data['comment'],
                }
            ), "text/html"
        )

        try:
            msg.send()
        except BadHeaderError as e:
            return HttpResponse(' '.join(
                ['BadHeaderError:'] + list(e.args)
            ))
        except Exception as e: # pragma: no cover
            print(e)
            return False
        return True
