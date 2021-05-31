from .models import *
from django.dispatch.dispatcher import receiver
from django.db.models.signals import post_save


@receiver(signal=post_save, sender=Loan)
def loan_post_save(sender, instance, **kwargs):
    Loan.objects.filter(id=instance.id).update(amount_left_to_repay=instance.get_amount_left_to_repay())

