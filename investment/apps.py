from django.apps import AppConfig


class InvestmentConfig(AppConfig):
    name = 'investment'

    def ready(self):
        from . import signals
