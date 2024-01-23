from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class Admin(AbstractUser):
    about_user = models.TextField(
        null=True, blank=True, verbose_name='درباره مدیر')

    class Meta:
        db_table ='admin'
        verbose_name = 'مدیر'
        verbose_name_plural = 'مدیران'

    def __str__(self):
        if self.first_name is not '' and self.last_name is not '':
            return self.get_full_name()
        return self.username