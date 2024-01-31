from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from user_module.models import User


# Create your models here.

class ProductCategory(models.Model):
    title = models.CharField(max_length=30, db_index=True, verbose_name='عنوان')
    url_title = models.CharField(max_length=30, db_index=True, verbose_name='عنوان در url')
    is_active = models.BooleanField(verbose_name='فعال / غیر فعال')
    is_delete = models.BooleanField(default=False, verbose_name='حذف شده / حذف نشده')

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'product_category'
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی ها'


class ProductBrand(models.Model):
    title = models.CharField(max_length=30, db_index=True, verbose_name='عنوان')
    url_title = models.CharField(max_length=30, db_index=True, verbose_name='عنوان در url')
    is_active = models.BooleanField(verbose_name='فعال / غیر فعال')

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'product_brand'
        verbose_name = 'برند'
        verbose_name_plural = 'برند ها'


class Product(models.Model):
    title = models.CharField(max_length=30, verbose_name='عنوان')
    category = models.ManyToManyField(
        ProductCategory,
        related_name='products_category',
        verbose_name='اطلاعات تکمیلی',
        db_table='products_category')
    image = models.ImageField(upload_to='images/products', null=True, blank=True, verbose_name='تصویر محصول')
    brand = models.ForeignKey(ProductBrand, on_delete=models.CASCADE, verbose_name='برند', null=True)
    price = models.IntegerField(verbose_name='قیمت')
    short_description = models.CharField(max_length=360, null=True, db_index=True, verbose_name='توضیحات کوتاه')
    description = models.TextField(db_index=True, verbose_name='توضیحات اصلی')
    slug = models.SlugField(
        default="",
        null=False,
        db_index=True,
        max_length=200,
        unique=True,
        verbose_name='عنوان در url')
    is_active = models.BooleanField(default=False, verbose_name='فعال / غیر فعال')
    is_delete = models.BooleanField(default=False, verbose_name='حذف شده / حذف نشده')


    def __str__(self):
        return self.title

    class Meta:
        db_table = 'product'
        verbose_name = 'محصول'
        verbose_name_plural = 'محصولات'


class ProductTag(models.Model):
    caption = models.CharField(max_length=30, db_index=True, verbose_name='عنوان')
    product_tags = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_tags')

    def __str__(self):
        return self.caption

    class Meta:
        db_table = 'product_tag'
        verbose_name = 'تگ محصول'
        verbose_name_plural = 'تگ های محصولات'


class ProductVisit(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, verbose_name='محصول')
    ip = models.CharField(max_length=30, verbose_name='آی پی کاربر')
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE, verbose_name='کاربر')

    def __str__(self):
        return f'{self.product.title} / {self.ip}'

    class Meta:
        db_table = 'product_visit'
        verbose_name = 'بازدید محصول'
        verbose_name_plural = 'بازدید های محصولات'


class ProductGallery(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='محصول')
    image = models.ImageField(upload_to='images/product-gallery',verbose_name='تصویر')

    def __str__(self):
        return self.product.title

    class Meta:
        db_table = 'product_gallery'
        verbose_name = 'تصویر گالری'
        verbose_name_plural = 'گالری تصاویر'


class ProductFavorite(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, verbose_name='محصول')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کاربر')

    def __str__(self):
        return self.product.title
    
    class Meta:
        db_table = 'product_favorite'
        verbose_name = 'محصول مورد علاقه'
        verbose_name_plural = 'محصولات مورد علاقه'
