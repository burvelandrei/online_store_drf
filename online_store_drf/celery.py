import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'online_store_drf.settings')

app = Celery('online_store_drf')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'send_discount_newsletter': {
        'task': 'your_app_name.tasks.send_discount_newsletter',
        'schedule': 60*60*24*7,  # 1 неделя
    },
}