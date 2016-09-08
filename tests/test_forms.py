import os
from django.core import mail
from django.test import TestCase
from .test_models import ok_fields


__all__ = ['ContactFormTest']


class ContactFormTest(TestCase):

    def setUp(self):
        self.data = ok_fields._asdict()
        self.bad = self.data.copy()
        del(self.bad['first_name'])


    def test_valid_form(self):
        response = self.client.post(
            '/contact/', self.data, follow=True
        )

        self.assertEqual(200,
            response.status_code
        )

        self.assertEqual(1,
            len(mail.outbox)
        )

        self.assertEqual(mail.outbox[0].subject,
            str(' '.join(('Contact Form:',
                self.data['first_name'],
                self.data['last_name'],
            )))
        )


    def test_invalid_form(self):
        response = self.client.post(
            '/contact/', self.bad, follow=True
        )

        self.assertEqual(200,
            response.status_code
        )

        self.assertFormError(response,
            'form', 'first_name', 'This field is required.'
        )
