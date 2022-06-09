from django.contrib.auth.models import User
from django.db import models
from account.models import Profile
from investment.models import UserInvestment

INVESTMENT_WITHDRAWAL_CHOICES = (
    ('pending', 'Pending'), ('disbursed', 'Disbursed'), ('declined', 'Declined'), ('approved', 'Approved')
)


class AdminNotification(models.Model):
    message = models.TextField()
    read = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Created: {self.created_on}, Read: {self.read}"

    class Meta:
        verbose_name_plural = 'Admin Notifications'


class InvestmentWithdrawal(models.Model):
    investment = models.ForeignKey(UserInvestment, on_delete=models.CASCADE)
    status = models.CharField(max_length=100, choices=INVESTMENT_WITHDRAWAL_CHOICES, default='pending')
    amount_requested = models.DecimalField(decimal_places=2, max_digits=20, default=0)
    narration = models.TextField(null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.investment} - {self.status}"




