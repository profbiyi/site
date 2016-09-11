import bleach
import markdown
from bs4 import BeautifulSoup
from datetime import datetime
from django.db import models
from django.conf import settings
from django.core import validators
from django.core.exceptions import ValidationError


STATUS_CHOICES = (
    ('r', 'Responded'),
    ('c', 'Closed'),
    ('n', 'New'),
)

_MARKDOWN_SETTINGS = {
    'ul_classes' : ['list-group'],
    'li_classes' : ['bullet-item'],
    'hx_classes' : ['text-primary'],
    'extensions': [
        'markdown.extensions.tables',
        'pymdownx.magiclink',
        'pymdownx.betterem',
        'pymdownx.tilde',
        'pymdownx.superfences',
    ],
}

def markup_markdown(md, allowed_tags=None):
    html = bleach.clean(markdown.markdown(
        md, extensions=list(getattr(settings,
            'MARKDOWN_EXTENSTIONS',
            _MARKDOWN_SETTINGS['extensions']
        ))), tags=allowed_tags or bleach.ALLOWED_TAGS + [
            'h%d' % i for i in range(1, 4)
        ] + ['p', 'div', 'pre']
    )
    soup = BeautifulSoup(
        '<div class="service-markup">%s</div>' % html,
        'html.parser'
    )
    for ul in soup.select('ul'):
        ul['class'] =  ' '.join(list(getattr(settings,
            'MARKDOWN_UL_CLASSES',
            _MARKDOWN_SETTINGS['ul_classes']
        )))
    for li in soup.select('ul li'):
        li['class'] = ' '.join(list(getattr(settings,
            'MARKDOWN_LI_CLASSES',
            _MARKDOWN_SETTINGS['li_classes']
        )))
    for h in ['h%d' % i for i in range(1, 4)]:
        for t in soup.select(h):
            t['class'] = ' '.join(list(getattr(settings,
                'MARKDOWN_HX_CLASSES',
                _MARKDOWN_SETTINGS['hx_classes']
            )))
    return str(soup)



class Service(models.Model):

    name = models.CharField(
        verbose_name='Service Name',
        max_length=100,
        unique=True,
    )

    description = models.TextField(
        verbose_name='Description',
        default='#'
    )

    html = models.TextField(
        verbose_name='HTML Markup',
    )

    order = models.IntegerField(
        null=True,
    )

    def save(self, *args, **kwargs):
        self.html = markup_markdown(self.description)
        if not self.order:
            self.order = getattr(
                Service.objects.last(), 'pk', 0
            ) + 1
        return super(Service, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.name)


class Contact(models.Model):

    class Meta:
        get_latest_by = "date"

    date = models.DateTimeField(
        auto_now_add=True
    )

    first_name = models.CharField(
        verbose_name='First Name',
        max_length=20,
        unique=False,
        validators=[
            validators.MinLengthValidator(2),
            validators.RegexValidator(
                '^[aA-zZ]+\Z$',
                message='Enter a valid first name.',
                code='invalid',
            ),
        ],
    )

    last_name = models.CharField(
        verbose_name='Last Name',
        max_length=20,
        unique=False,
        validators=[
            validators.MinLengthValidator(2),
            validators.RegexValidator(
                '^[aA-zZ]+$',
                message='Enter a valid last name.',
                code='invalid',
            ),
        ],
    )

    name = models.CharField(
        verbose_name='Full Name',
        max_length=100,
        blank=True,
        validators=[
            validators.MinLengthValidator(5),
            validators.RegexValidator(
                '[aA-zZ]+(?:[aA-zZ]+) [aA-zZ]+\Z',
                message='Enter a valid name (first & last, letters only).',
                code='invalid',
            ),
        ],
    )

    phone = models.CharField(
        verbose_name='Phone Number',
        max_length=10,
        validators=[
            validators.MinLengthValidator(10),
            validators.int_list_validator(
                sep='',
                message='Enter a valid phone number (Only Integers).'
            ),
        ],
    )

    email = models.CharField(
        verbose_name='Email Address',
        max_length=100,
        validators=[
            validators.EmailValidator(
                message='Enter a valid email.',
                code='invalid'
            ),
        ],
    )

    comment = models.TextField(
        verbose_name='Comment',
        validators=[
            validators.MinLengthValidator(4,
                message='Type at least 1 word (4 characters)',
            ),
        ]
    )

    status = models.CharField(
        default='n',
        max_length=1,
        choices=STATUS_CHOICES
    )

    notes = models.CharField(
        null=True,
        blank=True,
        verbose_name='Admin Notes',
        max_length=200
    )

    remote_address = models.GenericIPAddressField(
        verbose_name='Remote IP',
        null=True,
        blank=True
    )

    def save(self,  *args, **kwargs):
        if not self.name and (self.first_name and self.last_name):
            self.name = self.first_name + ' ' + self.last_name
        elif self.name: # pragma: no cover
            parts = self.name.split(' ')
            if len(parts) == 2:
                self.first_name = parts[0]
                self.last_name = parts[1]
            else:
                raise ValidationError("Bad name: '%s'" % self.name)

        name = self.name.split(' ')

        if self.name.split(' ') != [
            self.first_name, self.last_name
        ]: raise ValidationError("Bad names: '%s','%s','%s'" % (
            self.first_name, self.last_name, self.name
        ))

        return super(Contact, self).save(*args, **kwargs)

    def __str__(self):
        if self.date:
            return '{0} : {1}'.format(
                self.name,
                self.date.strftime('%Y-%m-%d %H:%M:%S')
            )
        return self.name
