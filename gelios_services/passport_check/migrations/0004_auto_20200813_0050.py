# Generated by Django 3.0.8 on 2020-08-12 21:50

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('passport_check', '0003_auto_20200813_0050'),
    ]

    operations = [
        migrations.AlterField(
            model_name='passport',
            name='PASSP_NUMBER',
            field=models.IntegerField(max_length=6, validators=[django.core.validators.RegexValidator('^\\d{1,10}$')]),
        ),
        migrations.AlterField(
            model_name='passport',
            name='PASSP_SERIES',
            field=models.IntegerField(max_length=4, validators=[django.core.validators.RegexValidator('^\\d{1,10}$')]),
        ),
    ]