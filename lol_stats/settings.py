"""
Django settings for lol_stats project.
This is presently dev/local settings.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

import os
from base import *

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS += (
    'debug_toolbar',
)

MIDDLEWARE_CLASSES += (
    # If debug_toolbar is installed app, but not included here, auto adds to front of list (good)
    #'debug_toolbar.middleware.DebugToolbarMiddleware',
)

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

db_pass = os.environ['LOL_STATS_DB_PASSWORD']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.path.join('lol_stats_db'),
        'USER': 'lol_stats',
        'PASSWORD': db_pass,
        'HOST': 'localhost',
        'PORT': '',
    }
}

# Set to IPs you will be viewing the site from that you want debug_toolbar to appear for.
INTERNAL_IPS = ('127.0.0.1',
                '10.0.2.2',)    # Address for host as seen from guest VM
