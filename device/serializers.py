
from rest_framework import serializers

from device.models import Device, Location


class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = '__all__'


class LocationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Location
        fields = '__all__'


class DeviceWithLastLocationSerializer(serializers.ModelSerializer):
    last_location_id = serializers.IntegerField()
    last_location_latitude = serializers.FloatField()
    last_location_longitude = serializers.FloatField()
    last_location_created_at = serializers.DateTimeField()

    class Meta:
        model = Device
        fields = ['id', 'last_location_id', 'last_location_latitude', 'last_location_longitude', 'last_location_created_at']

