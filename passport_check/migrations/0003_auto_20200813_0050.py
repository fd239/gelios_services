# Generated by Django 3.0.8 on 2020-08-12 21:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('passport_check', '0002_auto_20200730_1037'),
    ]

    operations = [
        migrations.RenameField(
            model_name='passport',
            old_name='number',
            new_name='PASSP_NUMBER',
        ),
        migrations.RenameField(
            model_name='passport',
            old_name='series',
            new_name='PASSP_SERIES',
        ),
    ]
