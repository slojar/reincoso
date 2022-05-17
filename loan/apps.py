from django.apps import AppConfig


class LoanConfig(AppConfig):
    name = 'loan'

    def ready(self):
        from . import crons
        from . import signals
