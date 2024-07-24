from celery import shared_task
from .models import Location, Device


@shared_task
def process_location_data(device_id, latitude, longitude):
    device, created = Device.objects.get_or_create(id=device_id)
    Location.objects.create(device=device, latitude=latitude, longitude=longitude)
