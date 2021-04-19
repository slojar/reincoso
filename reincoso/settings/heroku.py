import django_heroku
from .base import *
from decouple import config


SECRET_KEY = 'hFvHxrcgvkliePY0t+rkmklmPdZn29wv5aLF0t0WW/2w'

DEBUG = True

ALLOWED_HOSTS = []

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / config('DB_NAME', 'db.sqlite3'),
    }
}

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}

# Activate Django-Heroku.
django_heroku.settings(locals())

