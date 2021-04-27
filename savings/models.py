from django.db import models

# Create your models here.
from bot.choices import DAYS_OF_THE_MONTH_CHOICES
from bot.models import Profile


class Duration(models.Model):
    name = models.CharField(max_length=50, unique=True)
    interval = models.IntegerField(default=30, help_text='No. of days')

    def __str__(self):
        return f'{self.name} - {self.interval}days'


class Saving(models.Model):
    user = models.OneToOneField(Profile, on_delete=models.CASCADE)
    duration = models.ForeignKey(Duration, on_delete=models.SET_NULL, null=True, blank=True)
    amount = models.DecimalField(default=0.0, decimal_places=2, max_digits=20)
    total = models.DecimalField(default=0.0, decimal_places=2, max_digits=20)
    last_payment = models.DecimalField(default=0.0, decimal_places=2, max_digits=20)
    payment_day = models.CharField(max_length=20, choices=DAYS_OF_THE_MONTH_CHOICES, default='25')
    last_payment_date = models.DateTimeField(null=True, blank=True)
    next_payment_date = models.DateTimeField(null=True, blank=True)
    auto_save = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user} - {self.duration.name}'

