from django.db import models

from transaction.choices import PAYMENT_GATEWAYS
from .choices import *


class ActiveOnlyManager(models.Manager):
    def get_queryset(self):
        return super(ActiveOnlyManager, self).get_queryset().filter(active=True)


class InvestmentDuration(models.Model):
    title = models.CharField(max_length=50, default='')
    basis = models.CharField(max_length=50, choices=basis_type_choices, default="month")
    duration = models.IntegerField(default=1, help_text='This is the number of basis selected. If basis is monthly and basis number is 2, that means 2 months')
    number_of_days = models.IntegerField(default=30)
    percentage = models.DecimalField(decimal_places=2, max_digits=20, default=1)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title}: {self.number_of_days} day(s): {self.percentage}%"


class InvestmentType(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.CharField(max_length=100, unique=True, blank=True, null=True)
    description = models.TextField(null=True, blank=True)
    active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    objects = ActiveOnlyManager()

    def __str__(self):
        return f"{self.id}: {self.name}"


class Investment(models.Model):
    name = models.CharField(max_length=50, unique=True)
    type = models.ForeignKey(InvestmentType, on_delete=models.SET_NULL, null=True)
    description = models.TextField(null=True, blank=True)
    active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    objects = ActiveOnlyManager()

    def __str__(self):
        return f"{self.pk}: {self.name}"


class InvestmentOption(models.Model):
    investment = models.ForeignKey(Investment, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    duration = models.ForeignKey(InvestmentDuration, on_delete=models.SET_NULL, blank=True, null=True)
    active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    objects = ActiveOnlyManager()

    def __str__(self):
        return f"{self.pk}: {self.name}"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['investment', 'name'], name='investment_option_constraint'
            )
        ]


class InvestmentSpecification(models.Model):
    option = models.ForeignKey(InvestmentOption, on_delete=models.CASCADE)
    key = models.CharField(max_length=100, choices=INVESTMENT_SPEC_CHOICES)
    value = models.CharField(max_length=100)
    status = models.CharField(max_length=100, choices=AVAILABLE_INVESTMENT_STATUS_CHOICES, default='active')
    visible = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.pk}: {self.key}"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['option', 'key'], name='investment_spec_constraint'
            )
        ]


class UserInvestment(models.Model):
    user = models.ForeignKey("account.Profile", on_delete=models.CASCADE)
    investment = models.ForeignKey(Investment, on_delete=models.CASCADE, related_name='investment')
    option = models.ForeignKey(InvestmentOption, on_delete=models.CASCADE, related_name='option')
    duration = models.ForeignKey(InvestmentDuration, on_delete=models.CASCADE, related_name='investment_duration')
    amount_invested = models.DecimalField(decimal_places=2, max_digits=20, default=0)
    percentage = models.DecimalField(decimal_places=2, max_digits=20, default=0)
    return_on_invested = models.DecimalField(decimal_places=2, max_digits=20, default=0)
    amount_yield = models.DecimalField(decimal_places=2, max_digits=20, default=0)
    number_of_month = models.IntegerField(default=1)
    number_of_days = models.IntegerField(default=1)
    start_date = models.DateTimeField(null=True)
    end_date = models.DateTimeField(null=True)
    status = models.CharField(max_length=100, choices=INVESTMENT_STATUS_CHOICES, default='pending')
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.pk}: {self.user}"


class InvestmentTransaction(models.Model):
    user = models.ForeignKey("account.Profile", on_delete=models.CASCADE)
    user_investment = models.ForeignKey(UserInvestment, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=50, choices=TRANSACTION_TYPE_CHOICES, default='investment')
    amount = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    status = models.CharField(max_length=50, choices=TRANSACTION_STATUS_CHOICES, default='pending')
    payment_method = models.CharField(max_length=100, choices=PAYMENT_GATEWAYS, default='paystack')
    reference = models.CharField(max_length=100, null=True)
    response = models.TextField(null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"id: {self.id}:{self.user}: {self.transaction_type} - {self.amount}"





