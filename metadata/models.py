from django.db import models
from django.core import validators
from django.contrib.sites.models import Site
from django.contrib.postgres.fields import ArrayField


__all__ = [
    'Tag', 'Keyword', 'Link',
    'PostalAddress', 'PhoneNumber',
    'LocalBusiness', 'Website',
]


class Tag(models.Model):

    name = models.CharField(
        max_length=200
    )

    def __str__(self):
        return self.name


class Keyword(models.Model):

    name = models.CharField(
        max_length=200
    )

    def __str__(self):
        return self.name


class Link(models.Model):

    name = models.CharField(
        max_length=200
    )

    tags = models.ManyToManyField(
        Tag,
        blank=True
    )

    url = models.URLField(
        max_length=500,
        verbose_name='url'
    )

    def __str__(self):
        return self.url


class PostalAddress(models.Model):

    street = models.CharField(
        max_length=200,
        verbose_name='streetAddress'
    )

    locality = models.CharField(
        max_length=200,
        verbose_name='addressLocality'
    )

    region = models.CharField(
        max_length=200,
        verbose_name='addressRegion'
    )

    postal_code = models.CharField(
        max_length=200,
        verbose_name='postalCode'
    )

    def __str__(self):
        return "{0}\n{1},{2} {3}".format(
            self.street, self.locality,
            self.region, self.postal_code
        )

    class Meta:
        verbose_name_plural = "Postal Addresses"


class PhoneNumber(models.Model):

    kind = models.CharField(
        max_length=30,
        blank=True
    )

    country_code = models.CharField(
        max_length=3,
        blank=True,
    )

    area_code = models.CharField(
        max_length=3,
        validators=[
            validators.MinLengthValidator(3),
        ]
    )

    main_digits = models.CharField(
        max_length=10,
        validators=[
            validators.MinLengthValidator(7),
        ]
    )

    def __str__(self):
        return '({0}) {1}-{2}'.format(
            self.area_code,
            self.main_digits[:3],
            self.main_digits[3:]
        )


class Schema(models.Model):

    context = models.CharField(
        max_length=200,
        verbose_name='@context',
        default="http://schema.org"
    )

    class Meta:
        abstract = True


class Thing(Schema):

    name = models.CharField(
        max_length=200,
        verbose_name='name'
    )

    alt_name = models.CharField(
        max_length=200,
        verbose_name='alternateName',
        blank=True
    )

    description = models.TextField(
        verbose_name='description',
        blank=True
    )

    links = models.ManyToManyField(
        Link,
        verbose_name='sameAs',
    )

    url = models.URLField(
        verbose_name='url',
        blank=True
    )

    def __str__(self):
        return self.name

    class Meta(Schema.Meta):
        abstract = True


class Organization(Thing):

    address = models.ForeignKey(
        PostalAddress,
        verbose_name='address'
    )

    telephone = models.ForeignKey(
        PhoneNumber,
        on_delete=models.CASCADE
    )

    logo = models.URLField(
        verbose_name='logo',
        blank=True
    )

    founder = models.CharField(
        max_length=200,
        verbose_name='founder'
    )

    class Meta(Thing.Meta):
        abstract = True


class LocalBusiness(Organization):

    email = models.EmailField(
        verbose_name='email',
        blank=True
    )

    class Meta:
        verbose_name_plural = "Local Businesses"


class Website(models.Model):

    site = models.ForeignKey(
        Site,
        on_delete=models.CASCADE
    )

    schema = models.ForeignKey(
        LocalBusiness,
        on_delete=models.CASCADE
    )

    keywords = models.ManyToManyField(
        Keyword,
        verbose_name='keywords'
    )

    def __str__(self):
        return self.site.name
