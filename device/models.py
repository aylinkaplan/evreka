from django.db import models


class Device(models.Model):
    name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)


class Location(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    latitude = models.FloatField()
    longitude = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

