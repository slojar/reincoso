from django.contrib.auth.models import User
from django.db import models
from account.models import Profile


class AdminNotification(models.Model):
    message = models.TextField()
    read = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Admin Notifications'





