from django.contrib import admin
from . import models
from django.http import HttpRequest
# Register your models here.

class AdminPanel(admin.ModelAdmin):
    def save_model(self, request: HttpRequest, obj: models.Admin, form, change):
        if 'password' in form.changed_data:
            obj.set_password(form.cleaned_data['password'])
        return super().save_model(request, obj, form, change)


admin.site.register(models.Admin, AdminPanel)