from django.test import TestCase, Client
from landing.models import Contact
from django.core.exceptions import ValidationError
from collections import namedtuple


__all__ = ['LandingModelsTest']


ok_fields = namedtuple('Data', [
    'first_name','last_name','comment','email', 'phone'
])(
    'Foo', 'bar', 'hello world', 'foo@bar.com', '1231231234'
)


class LandingModelsTest(TestCase):

    def setUp(self):
        self.fields = ok_fields._asdict()

    def test_new_contact(self):
        c = Contact(**self.fields)
        c.full_clean()
        c.save()

    def test_bad_contact(self):
        self.fields.update({'email': ''})
        c = Contact(**self.fields)
        with self.assertRaises(ValidationError):
            c.full_clean()

    def test_changed_name_after_clean(self):
        c = Contact(**self.fields)
        c.full_clean()
        c.first_name = ''
        with self.assertRaises(ValidationError):
            c.save()
        c.first_name = 'Baz'
        c.save()
