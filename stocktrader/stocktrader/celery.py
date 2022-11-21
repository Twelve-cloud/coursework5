from celery.schedules import crontab
from celery import Celery
import os


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'stocktrader.settings')

app = Celery('stocktrader')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.beat_schedule = {
    'add-every-midnight':
    {
        'task': 'stocktrader.tasks.clear_database_from_waste_accounts',
        'schedule': crontab(minute=0, hour=0),
    },
    'update-every-month':
    {
        'task': 'stocktrader.tasks.update_users_balance',
        'schedule': crontab(minute='*/3')
    }
}

app.autodiscover_tasks()
