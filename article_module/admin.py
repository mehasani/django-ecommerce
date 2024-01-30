from django.contrib import admin
from django.http import HttpRequest

from . import models

# Register your models here.
from .models import Article


class ArticleCategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'url_title', 'parent', 'is_active']



class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active', 'author']

    def save_model(self, request: HttpRequest, obj: Article, form, change):
        if not change:
            obj.author = request.user
        return super().save_model(request, obj, form, change)


class ArticleCommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'create_date', 'show_comment', 'parent']
    readonly_fields = ['user']


admin.site.register(models.ArticleCategory, ArticleCategoryAdmin)
admin.site.register(models.Article, ArticleAdmin)
admin.site.register(models.ArticleComment, ArticleCommentAdmin)
