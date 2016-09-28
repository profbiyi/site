from django.contrib import admin
from .models import *


@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    list_display = ('name', 'url',)
    ordering = ('name',)


@admin.register(PostalAddress)
class PostalAddressAdmin(admin.ModelAdmin):
    pass


@admin.register(PhoneNumber)
class PhoneNumberAdmin(admin.ModelAdmin):
    pass


@admin.register(LocalBusiness)
class LocalBusinessAdmin(admin.ModelAdmin):
    pass


@admin.register(Keyword)
class KeywordAdmin(admin.ModelAdmin):
    pass


@admin.register(Website)
class WebsiteAdmin(admin.ModelAdmin):
    pass
