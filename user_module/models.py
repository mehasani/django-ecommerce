from django.db import models


# Create your models here.

class User(models.Model):
    user_levels = (
        ('normal', 'کاربرعادی'),
        ('vip', 'کاربر ویژه')
    )

    first_name = models.CharField(max_length=20, null=True, blank=True, verbose_name='نام کاربر')
    last_name = models.CharField(
        max_length=20, null=True, blank=True, verbose_name='نام خانوادگی کاربر')
    mobile = models.CharField(max_length=20, null=True, blank=True, verbose_name='تلفن همراه', unique=True)
    email = models.EmailField(max_length=100, verbose_name='ایمیل کاربر', unique=True)
    password = models.CharField(max_length=128, verbose_name='رمز عبور')
    level = models.CharField(
        max_length=30, choices=user_levels, null=True, blank=True, verbose_name='سطح کاربر')
    date_joined = models.DateTimeField(
        auto_now_add=True, editable=False, verbose_name='تاریخ ثبت نام')
    is_active = models.BooleanField(
        default=False, verbose_name='فعال / غیرفعال')
    email_active_code = models.CharField(
        max_length=100, verbose_name='کد فعال سازی ایمیل')
    address = models.TextField(null=True, blank=True, verbose_name='نشانی کاربر')

    class Meta:
        db_table ='user'
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربران'

    def __str__(self):
        if self.first_name is not '' and self.last_name is not '':
            return self.first_name + ' ' + self.last_name
        return self.email
