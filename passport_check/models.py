from django.core.validators import RegexValidator
from django.db import models


class Passport(models.Model):
    series = models.CharField(max_length=4)
    number = models.CharField(max_length=6)
