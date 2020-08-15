from django.core.validators import RegexValidator
from django.db import models


class Passport(models.Model):
    PASSP_SERIES = models.CharField(max_length=4)
    PASSP_NUMBER = models.CharField(max_length=6)
