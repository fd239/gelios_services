from django.db import models


class Passport(models.Model):
    series = models.IntegerField(max_length=4)
    number = models.IntegerField(max_length=6)
