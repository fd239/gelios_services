# Generated by Django 3.0.8 on 2020-07-29 14:05

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Passport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('series', models.IntegerField(max_length=4)),
                ('number', models.IntegerField(max_length=6)),
            ],
        ),
    ]
