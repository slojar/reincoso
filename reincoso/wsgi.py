import os
from django.core.wsgi import get_wsgi_application
from decouple import config


if config('env', '') == 'prod':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'reincoso.settings.prod')
else:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'reincoso.settings.dev')

application = get_wsgi_application()
