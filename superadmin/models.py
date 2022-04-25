from django.contrib.auth.models import User
from django.db import models
from account.models import Profile

STATUS_CHOICES = (
    ('pending', 'Pending'), ('successful', 'Successful'), ('failed', 'Failed')
)


class Transfer(models.Model):
    recipient_name = models.CharField(max_length=200)
    recipient_account_no = models.CharField(max_length=200)
    amount = models.FloatField(max_length=20)
    description = models.TextField()
    reference = models.CharField(max_length=200, blank=True, null=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='pending')
    updated_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    created_by = models.ForeignKey(User, null=True, blank=True, related_name='approved_by', on_delete=models.SET_NULL)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.recipient_name} - {self.amount}'





