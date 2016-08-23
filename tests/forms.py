from django.test import (
    TestCase, Client,
    override_settings,
    modify_settings,
)


__all__ = ['ContactFormTest']


class ContactFormTest(TestCase):

    def test_valid_form(self):
        response = self.client.post(
            '/contact/', {
                'first_name' : 'ryan',
                'last_name'  : 'kaiser',
                'phone'      : '2146641234',
                'email'      : 'foo@bar.com',
                'comment'    : 'hello world',
                'captcha'    : '123',
            }, follow=True
        )

        self.assertEqual(200, response.status_code)
        self.assertDictEqual({
            'captcha': ['This field is required.'],
        }, response.context_data.get('form').errors)

    def test_invalid_form(self):
        response = self.client.post(
            '/contact/', {
                'last_name'  : 'kaiser',
                'phone'      : '2146641234',
                'email'      : 'foo@bar.com',
                'comment'    : 'hello world',
                'captcha'    : '123',
            }, follow=True
        )

        self.assertEqual(200, response.status_code)
        self.assertDictEqual({
            'captcha': ['This field is required.'],
            'first_name': ['This field is required.'],
        }, response.context_data.get('form').errors)
