import os
import logging

from celery import Celery
from celery.signals import heartbeat_sent


# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'celery_django_sample.settings')

app = Celery('sample')

# Load task modules from all registered Django app configs.
app.config_from_object('django.conf:settings', namespace='CELERY')


@heartbeat_sent.connect
def heartbeat_sent_handler(sender=None, headers=None, body=None, **kwargs):
    import time

    logging.info("sleeping...")
    time.sleep(10)


# Auto-discover tasks from all installed apps.
app.autodiscover_tasks()
