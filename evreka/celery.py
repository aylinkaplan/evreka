import os
from celery import Celery

from evreka import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'evreka.settings')

app = Celery('evreka')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
