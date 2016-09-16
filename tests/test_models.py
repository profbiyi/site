import re
from django.test import TestCase, Client
from landing.models import Contact, Service, markup_markdown
from django.core.exceptions import ValidationError
from collections import namedtuple


ok_fields = namedtuple('Data', [
    'first_name','last_name','comment','email', 'phone'
])(
    'Foo', 'bar', 'hello world', 'foo@bar.com', '1231231234'
)


class LandingServiceModelTest(TestCase):

    fixtures = ['services.json']

    def test_markup_markdown(self):
        script_re = re.compile('<( +)?script')
        self.assertNotRegex(markup_markdown(self.description),
            script_re
        )
        self.assertRegex(self.description, script_re)

    def test_new_service(self):
        Service.objects.create(
            name='Test Service',
            description = "- foo\n- bar",
        )

    def test_save_with_explicit_order(self):
        last = Service.objects.last()
        s = Service(
            name='Test Service',
            description=self.description,
            order=last.order+1
        )
        s.save()
        self.assertEqual(s.order, last.order+1)

    @property
    def description(self):
        return """
# H1
## H2
### H3

<script>console.log("hello");</script>

- foo
- bar

```
<script>alert("Hello");</script>
<span class="foo">hello</span>
```

hello world
"""


class LandingContactModelTest(TestCase):

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
