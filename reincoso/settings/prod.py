import django_heroku
from .base import *
from decouple import config


SECRET_KEY = 'hFvHxrcgvkliePY0t+rkmklmPdZn29wv5aLF0t0WW/2w'

DEBUG = False

ALLOWED_HOSTS = []

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / config('DB_NAME', 'db.sqlite3'),
    }
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}

PAYSTACK_BASE_URL = 'https://api.paystack.co'
PAYSTACK_SECRET_KEY = 'sk_test_ac99347fc9b6c4deddc5aa6e2555b14ac1476fc4'
PAYSTACK_PUBLIC_KEY = 'pk_test_0d5259af2ab3bdac3f21f5a2dbc5903742aa0c62'

CORS_ALLOWED_ORIGINS = [
    "https://rent4less.herokuapp.com",
    "http://localhost:8080",
    "http://localhost:80",
    "http://localhost",
]

CORS_ALLOW_ALL_ORIGINS = True
# CSRF_TRUSTED_ORIGINS = CORS_ALLOWED_ORIGINS

cloudinary.config(
  cloud_name="codeadept",
  api_key="678643367988137",
  api_secret="QrgTgAvYw0nymzfjqn5_ZMPGbm4"
)

# TM30 Services
TM30_BASE_URL = 'https://services.tm30.net'
TM30_CLIENT_ID = 'live_d85469c795352d3fb60a'

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=2),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'UPDATE_LAST_LOGIN': True,
    'AUTH_HEADER_TYPES': ('Bearer', ),
}

# Activate Django-Heroku.
django_heroku.settings(locals())