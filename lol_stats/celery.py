from __future__ import absolute_import

import os

from celery import Celery

from django.conf import settings
from lol_stats.settings import BASE_DIR

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lol_stats.settings')

app = Celery('lol_stats',
             broker='amqp://',
             backend='db+sqlite:///' + BASE_DIR + '/db.sqlite3')

# Using a string here means the worker will not have to pick the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
