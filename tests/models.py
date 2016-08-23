from django.test import TestCase, Client
from landing.models import Contact
from django.core.exceptions import ValidationError

__all__ = ['LandingModelsTest']


class LandingModelsTest(TestCase):

    def test_new_contact(self):
        c = Contact(**self.ok_fields)
        c.full_clean()
        c.save()

    def test_bad_contact(self):
        fields = self.ok_fields.copy()
        fields.update({'email': ''})
        c = Contact(**fields)
        with self.assertRaises(ValidationError):
            c.full_clean()

    def test_changed_name_after_clean(self):
        fields = self.ok_fields.copy()
        c = Contact(**fields)
        c.full_clean()
        c.first_name = ''

        with self.assertRaises(ValidationError):
            c.save()

        c.first_name = 'Baz'
        c.save()

    @property
    def ok_fields(self):
        return {
            'first_name': 'Foo',
            'last_name' : 'Bar',
            'comment'   : 'hello world',
            'email'     : 'foo@bar.com',
            'phone'     : '1231231234',
        }
