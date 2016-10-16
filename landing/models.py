import re
from django.db import models
from django.utils.functional import cached_property
from landing.utils import markup_markdown


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
        blank=True
    )

    order = models.IntegerField(
        null=True,
    )

    @cached_property
    def html(self):
        return markup_markdown(
            self.description
        )

    @cached_property
    def anchor_id(self):
        return re.sub(
            " ?[&/\\@ ]+ ?", '_', self.name
        )[:30]

    def get_absolute_url(self):
        from django.urls import reverse
        return '%s#%s' % (reverse('services'), self.anchor_id)

    def save(self, *args, **kwargs):
        if not self.order:
            self.order = 1 + (
                Service.objects.aggregate(
                    n=models.Max('order')
                )['n'] or 0
            )
        return super(Service, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.name)
