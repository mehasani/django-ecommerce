from django.db import models


# Create your models here.

class SiteSetting(models.Model):
    site_name = models.CharField(max_length=200, verbose_name='نام سایت')
    site_url = models.CharField(max_length=200, verbose_name='دامنه سایت')
    address = models.CharField(max_length=200, null=True, blank=True, verbose_name='ادرس')
    phone = models.CharField(max_length=200, null=True, blank=True, verbose_name='تلفن')
    email = models.CharField(max_length=200, null=True, blank=True, verbose_name='ایمیل')
    about_us_text = models.TextField(verbose_name='متن درباره ما سایت')
    site_logo = models.ImageField(upload_to='images/site-setting', verbose_name='لوگو سایت')
    is_main_setting = models.BooleanField(verbose_name='تنظیمات اصلی')

    def __str__(self):
        return self.site_name

    class Meta:
        db_table='site_setting'
        verbose_name = 'تنظیمات سایت'
        verbose_name_plural = 'تنظیمات سایت'


class FooterLinkBox(models.Model):
    title = models.CharField(max_length=200, verbose_name='عنوان')

    def __str__(self):
        return self.title

    class Meta:
        db_table='footer_linkbox'
        verbose_name = 'دسته بندی صفحات فوتر'
        verbose_name_plural = 'دسته بندی های صفحات فوتر'


class FooterLink(models.Model):
    title = models.CharField(max_length=200, verbose_name='عنوان')
    url = models.CharField(max_length=500, verbose_name='لینک')
    footer_link_box = models.ForeignKey(to=FooterLinkBox, verbose_name='دسته بندی', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        db_table='footer_link'
        verbose_name = 'لینک فوتر'
        verbose_name_plural = 'لینک های فوتر'


class AdsBanner(models.Model):
    class AdsBannerPositions(models.TextChoices):
        product_list = 'product_list', 'صفحه لیست محصولات'
        product_detail = 'product_detail', 'صفحه جزئیات محصولات'
        about_us = 'about_us','صفحه درباره ما'
    title = models.CharField(max_length=200, verbose_name='عنوان بنر')
    url = models.URLField(max_length=500, null=True, blank=True, verbose_name='ادرس بنر')
    image = models.ImageField(upload_to='images/banners', verbose_name='تصویر بنر')
    is_active = models.BooleanField(verbose_name='فعال / غیر فعال')
    position = models.CharField(max_length=200,choices=AdsBannerPositions.choices, verbose_name='جایگاه نمایشی')

    def __str__(self):
        return self.title

    class Meta:
        db_table='ads_banner'
        verbose_name = 'بنر تبلیغاتی'
        verbose_name_plural = 'بنر های تبلیغاتی'
