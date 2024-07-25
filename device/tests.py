import json

from django.test import TestCase
from rest_framework.test import APIClient

from device.models import Device, Location


class DeviceLocationSetupTestCase(TestCase):
    def setUp(self):
        self.device1 = Device.objects.create(name="Device 1")
        self.device2 = Device.objects.create(name="Device 2")

        # Create locations for device1
        self.location1 = Location.objects.create(
            device=self.device1,
            latitude=40.7128,
            longitude=-74.0060
        )
        self.last_location1 = Location.objects.create(
            device=self.device1,
            latitude=41.8781,
            longitude=-87.6298,
        )
        # Create locations for device2
        self.location2 = Location.objects.create(
            device=self.device2,
            latitude=34.0522,
            longitude=-118.2437,
        )
        self.last_location2 = Location.objects.create(
            device=self.device2,
            latitude=37.7749,
            longitude=-122.4194,
        )

    def test_device_creation(self):
        self.assertEqual(Device.objects.count(), 2)

    def test_location_creation(self):
        self.assertEqual(Location.objects.count(), 4)

    def test_location_history(self):
        api_client = APIClient()
        url = f'/devices/{self.device1.id}/location_history/'
        response = api_client.get(url)
        response_json = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        response_data = set([item.get('id') for item in response_json])
        location_data = {self.location1.id, self.last_location1.id}
        self.assertEqual(response_data, location_data)

    def test_last_locations(self):
        api_client = APIClient()
        url = f'/devices/last_locations/'
        response = api_client.get(url)
        response_json = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        response_data = set([item.get('last_location_id') for item in response_json])
        location_data = {self.last_location1.id, self.last_location2.id}
        self.assertEqual(response_data, location_data)
