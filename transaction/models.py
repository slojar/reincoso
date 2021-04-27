from django.db import models
from bot.models import Profile, Saving
from .choices import PAYMENT_GATEWAYS, TRANSACTION_STATUS


class SavingTransaction(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    saving = models.ForeignKey(Saving, on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=100, choices=PAYMENT_GATEWAYS, default='paystack')
    amount = models.DecimalField(decimal_places=2, max_digits=20, default=0)
    reference = models.CharField(max_length=100, null=True)
    status = models.CharField(max_length=50, choices=TRANSACTION_STATUS)
    response = models.TextField(null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"id: {self.pk}, user: {self.user}, amount: {self.amount}, status: {self.status}"