from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from .models import *


@receiver(signal=post_save, sender=Profile)
def create_member_id(sender, instance, **kwargs):
    if not instance.member_id:
        instance.member_id = slugify(f'REN{instance.id}{str(uuid.uuid4())[:6]}')
        instance.save()


@receiver(signal=post_delete, sender=Profile)
def profile_post_save(sender, instance, **kwargs):
    User.objects.filter(id=instance.user_id).delete()


