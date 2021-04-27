from django.db import models
from bot.models import Profile
from .choices import *


class LoanDuration(models.Model):
    duration = models.CharField(max_length=50, unique=True)
    number_of_days = models.IntegerField(default=1)
    percentage = models.DecimalField(decimal_places=2, max_digits=20, default=1, help_text="E.g: 1 means 1%, 10 means 10%")
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.duration}: {self.number_of_days} day(s)"


class Loan(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    duration = models.ForeignKey(LoanDuration, on_delete=models.SET_NULL, null=True)
    number_of_days = models.IntegerField(default=1)
    percentage = models.DecimalField(decimal_places=2, max_digits=20, default=1)
    amount_to_repay = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    amount_repaid = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    start_date = models.DateTimeField(null=True)
    end_date = models.DateTimeField(null=True)
    last_repayment_date = models.DateTimeField(null=True, blank=True)
    next_repayment_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=50, choices=loan_status_choices, default='pending')

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user}: {self.amount}"


class LoanTransaction(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=50, choices=loan_transaction_type_choices, default='repayment')
    amount = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    status = models.CharField(max_length=50, choices=loan_transaction_status_choices, default='pending')
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"id: {self.id}:{self.user}: {self.transaction_type} - {self.amount}"

    





