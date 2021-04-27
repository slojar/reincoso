import django_heroku
from .base import *
from decouple import config


SECRET_KEY = 'reincoso'

DEBUG = True

ALLOWED_HOSTS = []

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / config('DB_NAME', 'db.sqlite3'),
    }
}

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS':
        'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 100,
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
}

PAYSTACK_BASE_URL = 'https://api.paystack.co'
PAYSTACK_SECRET_KEY = 'sk_test_9b3d455a84aa3da9bf0a7610a80529dc524c377d'
PAYSTACK_PUBLIC_KEY = 'pk_test_db348e565111ebfbc63e12ca0ad9f73d8eb93a98'

# Activate Django-Heroku.
django_heroku.settings(locals())

