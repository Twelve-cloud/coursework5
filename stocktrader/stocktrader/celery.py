from celery import Celery
import os


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'stocktrader.settings')

app = Celery('stocktrader')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()
