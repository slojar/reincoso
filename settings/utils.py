from .models import *


def general_settings():
    settings, created = GeneralSettings.objects.get_or_create(site=Site.objects.get_current())
    return settings
