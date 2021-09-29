from django.db import models
from account.choices import DAYS_OF_THE_MONTH_CHOICES
from account.models import Profile
from transaction.choices import PAYMENT_GATEWAYS, TRANSACTION_STATUS
from .choices import *


class Duration(models.Model):
    name = models.CharField(max_length=50, unique=True)
    number_of_day = models.IntegerField(default=30, help_text='No. of days')
    number_of_month = models.IntegerField(default=1, help_text='No. of months')

    def __str__(self):
        return f'{self.name} - {self.number_of_day}days'


class SavingsType(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.id}: {self.name}"


class Saving(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    type = models.ForeignKey(SavingsType, on_delete=models.SET_NULL, null=True)
    duration = models.ForeignKey(Duration, on_delete=models.SET_NULL, null=True, blank=True)
    amount = models.DecimalField(default=0.0, decimal_places=2, max_digits=20)
    total = models.DecimalField(default=0.0, decimal_places=2, max_digits=20)
    payment_day = models.CharField(max_length=5, choices=DAYS_OF_THE_MONTH_CHOICES, default='30')
    last_payment = models.DecimalField(default=0.0, decimal_places=2, max_digits=20)
    last_payment_date = models.DateTimeField(null=True, blank=True)
    next_payment_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=50, default='pending', choices=SAVINGS_STATUS_CHOICES)
    auto_save = models.BooleanField(default=True)
    payment_gateway = models.CharField(max_length=50, choices=PAYMENT_GATEWAYS, default='paystack')
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user} - {self.duration.name if self.duration else None}'


class SavingTransaction(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    saving = models.ForeignKey(Saving, on_delete=models.CASCADE)
    payment_gateway = models.CharField(max_length=100, choices=PAYMENT_GATEWAYS, default='paystack')
    amount = models.DecimalField(decimal_places=2, max_digits=20, default=0)
    reference = models.CharField(max_length=100, null=True)
    status = models.CharField(max_length=50, choices=TRANSACTION_STATUS)
    response = models.TextField(null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"id: {self.pk}, user: {self.user}, amount: {self.amount}, status: {self.status}"

    class Meta:
        ordering = ['-id']

