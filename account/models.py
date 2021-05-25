from django.db import models
from django.contrib.auth.models import User
from .choices import *
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.utils.text import slugify
import uuid


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20)
    bvn = models.CharField(max_length=20)
    member_id = models.CharField(max_length=200, editable=False, blank=True, null=True)
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES, default='male')
    status = models.CharField(max_length=20, choices=ACTIVE_STATUS_CHOICES, default='active')
    paid_membership_fee = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user} - {self.member_id}'


@receiver(signal=post_save, sender=Profile)
def create_member_id(sender, instance, **kwargs):
    if not instance.member_id:
        instance.member_id = slugify(f'REN{instance.id}{str(uuid.uuid4())[:6]}')
        instance.save()


class FaqCategory(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Faq Categories'


class Faq(models.Model):
    question = models.CharField(max_length=200)
    answer = models.TextField()
    category = models.ForeignKey(FaqCategory, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.question


class FeedbackMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name} - {self.subject}'


class LoanGuarantor(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    guarantor = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, related_name='guarantor')

    def __str__(self):
        return f"{self.user}: {self.guarantor}"

