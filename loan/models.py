from django.db import models

from account.models import Profile
from .choices import *
from django.contrib.sites.models import Site
from savings.models import PAYMENT_GATEWAYS


basis_type_choices = (
    ('weekly', 'Weekly'), ('monthly', 'Monthly'), ('yearly', 'Yearly'),
)


class LoanDuration(models.Model):
    title = models.CharField(max_length=50, default='')
    basis = models.CharField(max_length=50, choices=basis_type_choices, default="month")
    duration = models.IntegerField(default=1, help_text='This is the number of basis selected. If basis is '
                                                            'monthly and basis number is 2, that means 2 months')
    number_of_days = models.IntegerField(default=1)
    percentage = models.DecimalField(decimal_places=2, max_digits=20, default=20)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title}: {self.number_of_days} day(s)"


class Loan(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    duration = models.ForeignKey(LoanDuration, on_delete=models.SET_NULL, null=True)
    basis = models.CharField(max_length=50, choices=basis_type_choices, default='monthly')
    basis_duration = models.IntegerField(default=0)
    number_of_days = models.IntegerField(default=1)
    percentage = models.DecimalField(decimal_places=2, max_digits=20, default=1)
    percentage_amount = models.DecimalField(decimal_places=2, max_digits=20, default=1)
    amount_to_repay = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    amount_repaid = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    amount_left_to_repay = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    amount_to_repay_split = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    start_date = models.DateTimeField(null=True)
    end_date = models.DateTimeField(null=True)
    last_repayment_date = models.DateTimeField(null=True, blank=True)
    next_repayment_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=50, choices=loan_status_choices, default='pending')

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user}: {self.amount}"

    def get_amount_left_to_repay(self):
        amt_to_repay = self.amount_to_repay
        amt_repaid = self.amount_repaid
        return float(amt_to_repay - amt_repaid)


class LoanTransaction(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=50, choices=loan_transaction_type_choices, default='repayment')
    amount = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    status = models.CharField(max_length=50, choices=loan_transaction_status_choices, default='pending')
    payment_method = models.CharField(max_length=100, choices=PAYMENT_GATEWAYS, default='paystack')
    reference = models.CharField(max_length=100, null=True)
    response = models.TextField(null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return f"id: {self.id}:{self.user}: {self.transaction_type} - {self.amount}"

    





