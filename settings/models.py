from django.db import models
from django.contrib.sites.models import Site


class GeneralSettings(models.Model):
    site = models.ForeignKey(Site, on_delete=models.CASCADE)
    site_name = models.CharField(max_length=200)
    site_link = models.URLField(null=True, blank=True)
    membership_fee = models.DecimalField(decimal_places=2, max_digits=20, default=1000)

    def __str__(self):
        return f"{self.site}"

    class Meta:
        verbose_name_plural = 'General Settings'


class PaymentGateway(models.Model):
    site = models.ForeignKey(GeneralSettings, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=50)
    slug = models.CharField(max_length=100, null=True)

    def __str__(self):
        return f"{self.name}"


class LoanSetting(models.Model):
    site = models.OneToOneField(Site, on_delete=models.SET_NULL, null=True)
    eligibility_days = models.IntegerField(default=180, help_text='This is the number of days user must have saved '
                                                                  'before eligible for loan')
    maximum_loan = models.IntegerField(default=1, help_text='This is the maximum time a user can apply for loan when '
                                                            'one is still active')
    offer = models.DecimalField(max_digits=20, decimal_places=2, default=3, help_text='This will be multiplied by user '
                                                                                      'savings amount')
    number_of_guarantor = models.PositiveIntegerField(default=0, help_text='This is the number of guarantor(s) a user '
                                                                           'must have to be eligible for a loan')

    def __str__(self):
        return f"{self.site}"

