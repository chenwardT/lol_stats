"""
Django settings for lol_stats project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

from riotwatcher import riotwatcher

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Following keys are stored as environment vars and in try blocks so RTD doesn't scream.

# my Riot API key (keep secret!)
try:
    riot_api = riotwatcher.RiotWatcher(os.environ['RIOT_API_KEY'])
except KeyError:
    pass

# SECURITY WARNING: keep the secret key used in production secret!
try:
    SECRET_KEY = os.environ['DJANGO_SECRET_KEY']
except KeyError:
    pass

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'debug_toolbar',
    'django_extensions',
    'rest_framework',
    'api',
    'summoner',
    'champion',
    'item',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'lol_stats.urls'

WSGI_APPLICATION = 'lol_stats.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

# was True previously (default now?)
USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
    #'/usr/share/nginx/www/static/'
)

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'lol_stats/templates'),
)

REST_FRAMEWORK = {
    'PAGINATE_BY': 10,
}

# Set to IPs you will be viewing the site from that you want debug_toolbar to appear for.
#INTERNAL_IPS = ('10.0.2.2',)
