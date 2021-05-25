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

    def first_name(self):
        return self.user.first_name or None

    def last_name(self):
        return self.user.last_name or None

    def email(self):
        return self.user.email or None

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


class Guarantor(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, name='user')
    guarantor = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, related_name='user_guarantor')
    confirmed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user}: {self.guarantor}"


class UserCard(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    email = models.EmailField()
    bank = models.CharField(max_length=50, null=True)
    card_type = models.CharField(max_length=50, null=True)
    bin = models.CharField(max_length=50, null=True)
    last4 = models.CharField(max_length=50, null=True)
    exp_month = models.CharField(max_length=2, null=True)
    exp_year = models.CharField(max_length=4, null=True)
    signature = models.CharField(max_length=200, null=True)
    authorization_code = models.CharField(max_length=200, null=True)
    payload = models.TextField(null=True)
    default = models.BooleanField(default=False, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user}"



