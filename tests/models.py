from django.test import TestCase, Client
from landing.models import Contact


__all__ = ['LandingModelsTest']


class LandingModelsTest(TestCase):

    def test_new_contact(self):
        Contact(**self.ok_fields).save()

    def test_bad_contact(self):
        fields = self.ok_fields.copy()
        del(fields['email'])
        Contact(**fields).save()

    @property
    def ok_fields(self):
        return {
            'first_name': 'Foo',
            'last_name' : 'Bar',
            'comment'   : 'hello world',
            'email'     : 'foo@bar.com',
            'phone'     : '1231231234',
        }
