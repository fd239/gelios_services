# Generated by Django 3.0.8 on 2020-08-16 17:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('passport_check', '0008_passport_num_series'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='passport',
            name='NUM_SERIES',
        ),
    ]