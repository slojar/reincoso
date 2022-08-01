import django_heroku
from .base import *
from decouple import config
import logging
import environ

env = environ.Env()
environ.Env.read_env(os.path.join('.env'))

SECRET_KEY = env('SECRET_KEY')

DEBUG = True

# ALLOWED_HOSTS = ['*']
ALLOWED_HOSTS = []

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': "d2g9vc9qhqk11p",
        'USER': "oufhmuryqtsroa",
        'PASSWORD': "5ab865b7eeb173c123d306829d55c362c1cf18c60013d8fde5e727c89b4ff0d4",
        'HOST': "ec2-54-217-15-9.eu-west-1.compute.amazonaws.com",
        'PORT': "5432",
    }
}

# PAYSTACK CREDENTIALS
PAYSTACK_BASE_URL = env('PAYSTACK_BASE_URL')
PAYSTACK_SECRET_KEY = env('PAYSTACK_SECRET_KEY')
PAYSTACK_PUBLIC_KEY = env('PAYSTACK_PUBLIC_KEY')
PAYSTACK_REF = env('PAYSTACK_REF')
PAYSTACK_TEST_CHARGE = env('PAYSTACK_TEST_CHARGE')

# SENDING EMAIL CREDENTIALS
EMAIL_API_URL = env('EMAIL_API_URL')
EMAIL_API_KEY = env('EMAIL_API_KEY')
EMAIL_SENDER = env('EMAIL_SENDER')

CALLBACK_URL = env("CALLBACK_URL")

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

CORS_ALLOWED_ORIGINS = [
    "https://reincoso.herokuapp.com",
    "http://localhost:8080",
    "http://localhost:80",
    "http://localhost",
]

CORS_ALLOW_ALL_ORIGINS = True

# Activate Django-Heroku.
django_heroku.settings(locals())

