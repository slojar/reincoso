from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils.text import slugify

from .models import *


@receiver(signal=pre_save, sender=InvestmentType)
def investment_type_post_save(sender, instance, **kwargs):
    instance.slug = slugify(instance.name)

