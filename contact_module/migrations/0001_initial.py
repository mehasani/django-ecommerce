# Generated by Django 4.2.6 on 2024-01-29 17:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ContactUs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(db_index=True, max_length=30, verbose_name='عنوان')),
                ('email', models.EmailField(max_length=300, verbose_name='ایمیل')),
                ('full_name', models.CharField(max_length=300, verbose_name='نام و نام خانوادگی')),
                ('message', models.TextField(verbose_name='متن تماس با ما')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')),
                ('response', models.TextField(blank=True, null=True, verbose_name='متن پاسخ تماس با ما')),
                ('is_read_by_admin', models.BooleanField(default=False, verbose_name='خوانده شده توسط ادمین')),
            ],
            options={
                'verbose_name': 'تماس با ما',
                'verbose_name_plural': 'لیست تماس با ما',
                'db_table': 'contact',
            },
        ),
    ]
