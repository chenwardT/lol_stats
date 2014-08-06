from __future__ import absolute_import

import os

from celery import Celery
#print celery.__file__

from django.conf import settings
from lol_stats.base import BASE_DIR, get_env_variable

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lol_stats.development')

DB_PASSWORD = get_env_variable('LOL_STATS_DB_PASSWORD')

print DB_PASSWORD

app = Celery('lol_stats',
             broker='amqp://',
             backend='db+postgresql://lol_stats:' + DB_PASSWORD + '@localhost/lol_stats_db')

# Using a string here means the worker will not have to pick the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
