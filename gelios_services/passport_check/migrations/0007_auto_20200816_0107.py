# Generated by Django 3.0.8 on 2020-08-15 22:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('passport_check', '0006_auto_20200816_0104'),
    ]

    operations = [
        migrations.AlterField(
            model_name='passport',
            name='PASSP_NUMBER',
            field=models.CharField(max_length=6),
        ),
    ]
