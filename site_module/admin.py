from django.contrib import admin
from . import models


# Register your models here.

class FooterLinkAdmin(admin.ModelAdmin):
    list_display = ['title', 'url']


class AdsBannerAdmin(admin.ModelAdmin):
    list_display = ['title', 'position', 'is_active']


admin.site.register(models.SiteSetting)
admin.site.register(models.FooterLinkBox)
admin.site.register(models.FooterLink, FooterLinkAdmin)
admin.site.register(models.AdsBanner, AdsBannerAdmin)
