from django.db import models


class Music(models.Model):
    name = models.CharField(max_length=256)
    style = models.CharField(max_length=32)


class TemperatureLocation(models.Model):
    location = models.CharField(max_length=128)
    style = models.CharField(max_length=32)
    last_update_time = models.DateTimeField()
