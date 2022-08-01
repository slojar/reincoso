import django_heroku
from .base import *
from decouple import config
import dj_database_url
import logging
import environ

env = environ.Env()
environ.Env.read_env(os.path.join('.env'))


SECRET_KEY = env('SECRET_KEY')

DEBUG = False

ALLOWED_HOSTS = ['*', 'api.reincosocoop.com']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': env('DATABASE_NAME'),
        'USER': env('DATABASE_USER'),
        'PASSWORD': env('DATABASE_PASSWORD'),
        'HOST': env('DATABASE_HOST'),
        'PORT': env('DATABASE_PORT'),
    }
}

PAYSTACK_BASE_URL = env('PAYSTACK_BASE_URL')
PAYSTACK_SECRET_KEY = env('PAYSTACK_SECRET_KEY')
PAYSTACK_PUBLIC_KEY = env('PAYSTACK_PUBLIC_KEY')
PAYSTACK_REF = env('PAYSTACK_REF')
PAYSTACK_TEST_CHARGE = env('PAYSTACK_TEST_CHARGE')

EMAIL_API_URL = env('EMAIL_API_URL')
EMAIL_API_KEY = env('EMAIL_API_KEY')
EMAIL_SENDER = env('EMAIL_SENDER')

CALLBACK_URL = env("CALLBACK_URL")

#CORS_ALLOWED_ORIGINS = [
#    "http://reincosocoop.com"
#    "https://reincosocoop.com"
#    "http://api.reincosocoop.com"
#    "https://api.reincosocoop.com"
#    "http://admin.reincosocoop.com"
#    "https://admin.reincosocoop.com"
#    "http://bot.reincosocoop.com"
#    "https://bot.reincosocoop.com"
#]

CORS_ALLOW_ALL_ORIGINS = True
# CSRF_TRUSTED_ORIGINS = CORS_ALLOWED_ORIGINS


SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=2),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': True,

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,

    'AUTH_HEADER_TYPES': ('Bearer', "Token"),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',

    'JTI_CLAIM': 'jti',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')


