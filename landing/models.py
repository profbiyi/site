import re
import bleach
import markdown
from bs4 import BeautifulSoup
from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.encoding import smart_text
from django.utils.functional import cached_property


_MARKDOWN_SETTINGS = {
    'ul_classes' : ['list-group'],
    'li_classes' : ['bullet-item'],
    'hx_classes' : ['text-primary'],
    'extensions': [
        'markdown.extensions.tables',
        'markdown.extensions.abbr',
        'markdown.extensions.smarty',
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
        '<div class="service-markup">\n%s\n</div>' % html,
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

    class Meta:
        ordering = ('order',)

    name = models.CharField(
        verbose_name='Service Name',
        max_length=100,
        unique=True,
    )

    description = models.TextField(
        verbose_name='Description',
        default='#'
    )

    order = models.IntegerField(
        null=True,
    )

    @cached_property
    def html(self):
        return markup_markdown(self.description) if (
            self.description
        ) else None

    @cached_property
    def anchor_id(self):
        return re.sub(
            " ?[&/\\@ ] ?", '_', self.name
        )[:30] if self.name else str()

    def get_absolute_url(self):
        from django.urls import reverse
        return '%s#%s' % (reverse('services'), self.anchor_id)

    def save(self, *args, **kwargs):
        if not self.order:
            self.order = getattr(
                Service.objects.last(), 'pk', 0
            ) + 1
        return super(Service, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.name)
