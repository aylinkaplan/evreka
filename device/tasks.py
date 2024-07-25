from celery import shared_task

from .models import Location, Device


@shared_task
def process_location_data(external_id, latitude, longitude):
    device, created = Device.objects.get_or_create(external_id=external_id)
    Location.objects.create(device=device, latitude=latitude, longitude=longitude)
