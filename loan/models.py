from django.db import models
from account.models import Profile
from .choices import *
from django.contrib.sites.models import Site

basis_type_choices = (
    ('weekly', 'Weekly'), ('monthly', 'Monthly'), ('yearly', 'Yearly'),
)


class LoanSetup(models.Model):
    site = models.OneToOneField(Site, on_delete=models.SET_NULL, null=True)
    eligibility_days = models.IntegerField(default=180, help_text='This is the number of days user must have saved '
                                                                  'before eligible for loan')
    maximum_loan = models.IntegerField(default=1, help_text='This is the maximum time a user can apply for loan when '
                                                            'one is still active')
    offer = models.DecimalField(max_digits=20, decimal_places=2, default=3, help_text='This will be multiplied by user '
                                                                                      'savings amount')

    def __str__(self):
        return f"{self.site}"


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

    





