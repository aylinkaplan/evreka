from django.db import models


class Device(models.Model):
    external_id = models.CharField(unique=True, max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)


class Location(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    latitude = models.FloatField()
    longitude = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

