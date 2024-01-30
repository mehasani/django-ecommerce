from rest_framework import serializers
from jalali_date import datetime2jalali
from admin_module.models import Admin
from .models import Article, ArticleCategory


class AdminArticleCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleCategory
        fields = ['id', 'title']

class AdminArticleSerializer(serializers.ModelSerializer):
    create_date_jalali = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = ['id', 'title', 'slug', 'image', 'short_description', 'author', 'text', 'is_active', 'create_date',
                  'selected_categories', 'create_date_jalali']

    def get_create_date_jalali(self, obj):
        create_date_jalali = datetime2jalali(obj.create_date)
        return create_date_jalali.strftime('%Y-%m-%d')

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['author'] = user
        selected_categories_data = validated_data.pop('selected_categories', [])
        article = Article.objects.create(**validated_data)
        article.selected_categories.set(selected_categories_data)
        return article


class ArticleSerializer(serializers.ModelSerializer):
    jalali_date = serializers.SerializerMethodField()
    author_name = serializers.CharField(source='author')

    class Meta:
        model = Article
        fields = ['id', 'title', 'slug', 'image', 'short_description', 'author_name', 'is_active', 'jalali_date']

    def get_jalali_date(self, obj):
        jalali_date = datetime2jalali(obj.create_date)
        return jalali_date.strftime('%Y-%m-%d')