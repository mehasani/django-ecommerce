from django.db import models


# Create your models here.

class Slider(models.Model):
    title = models.CharField(max_length=200, verbose_name='عنوان')
    description = models.CharField(max_length=500, verbose_name='توضیحات اسلایدر')
    image = models.ImageField(upload_to='images/sliders', verbose_name='تصویر اسلایدر')
    url = models.URLField(max_length=200, verbose_name='لینک')
    url_title = models.CharField(max_length=200, verbose_name='عنوان لینک')
    is_active = models.BooleanField(default=True, verbose_name='فعال / غیر فعال')

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'slider'
        verbose_name = 'اسلایدر'
        verbose_name_plural = 'اسلایدرها'
