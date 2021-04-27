from django.db import models

# Create your models here.
from bot.choices import DAYS_OF_THE_MONTH_CHOICES
from bot.models import Profile


class Duration(models.Model):
    name = models.CharField(max_length=50)
    interval = models.IntegerField(default=30, help_text='No. of days')

    def __str__(self):
        return f'{self.name} - {self.interval}days'


class Saving(models.Model):
    user = models.OneToOneField(Profile, on_delete=models.CASCADE)
    duration = models.ForeignKey(Duration, on_delete=models.SET_NULL, null=True, blank=True)
    fixed_payment = models.FloatField(default=0.0, null=True, blank=True)
    last_payment = models.FloatField(default=0.0, null=True, blank=True)
    last_payment_date = models.DateTimeField(null=True, blank=True)
    next_payment_date = models.DateTimeField(null=True, blank=True)
    balance = models.FloatField(default=0.0, null=True, blank=True)
    repayment_day = models.CharField(max_length=20, choices=DAYS_OF_THE_MONTH_CHOICES, default='25')
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user} - {self.duration.name}'