from django.db import models


INVESTMENT_SPEC_CHOICES = (
    ('key metric', "Key metric"), ('minimum return', "Minimum return"),
    ('target for return per annum', "Target for return per annum"),
    ('investible asset claim', "Investible asset claim"),
    ('30 days average return', "30 days average return"),
    ('return on investment', "Return on investment"),
)

AVAILABLE_INVESTMENT_STATUS_CHOICES = (
    ('active', 'Active'), ('inactive', 'Inactive'),
)

basis_type_choices = (
    ('weekly', 'Weekly'), ('monthly', 'Monthly'), ('yearly', 'Yearly'),
)

INVESTMENT_STATUS_CHOICES = (
    ('pending', 'Pending'), ('approved', 'Approved'), ('ongoing', 'Ongoing'), ('completed', 'Completed'),
    ('rejected', 'Rejected'), ('cancelled', 'Cancelled'), ('failed', 'Failed'),
)


class InvestmentDuration(models.Model):
    title = models.CharField(max_length=50, default='')
    basis = models.CharField(max_length=50, choices=basis_type_choices, default="month")
    duration = models.IntegerField(default=1, help_text='This is the number of basis selected. If basis is monthly and basis number is 2, that means 2 months')
    number_of_days = models.IntegerField(default=30)
    percentage = models.DecimalField(decimal_places=2, max_digits=20, default=1)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title}: {self.number_of_days} day(s)"


class AvailableInvestment(models.Model):
    name = models.CharField(max_length=50, unique=True)
    status = models.CharField(max_length=50, choices=AVAILABLE_INVESTMENT_STATUS_CHOICES, default='active')
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.pk}: {self.name}"


class InvestmentOption(models.Model):
    available_investment = models.ForeignKey(AvailableInvestment, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    duration = models.ForeignKey(InvestmentDuration, on_delete=models.CASCADE, null=True, blank=True)
    status = models.CharField(max_length=100, choices=AVAILABLE_INVESTMENT_STATUS_CHOICES, default='active')
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.pk}: {self.name}"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['available_investment', 'name'], name='investment_option_constraint'
            )
        ]


class InvestmentSpecification(models.Model):
    investment_option = models.ForeignKey(InvestmentOption, on_delete=models.CASCADE)
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
                fields=['investment_option', 'key'], name='investment_spec_constraint'
            )
        ]


class Investment(models.Model):
    user = models.ForeignKey("account.Profile", on_delete=models.CASCADE)
    investment = models.ForeignKey(AvailableInvestment, on_delete=models.CASCADE, related_name='investment')
    option = models.ForeignKey(InvestmentOption, on_delete=models.CASCADE, related_name='option')
    duration = models.ForeignKey(InvestmentDuration, on_delete=models.CASCADE, related_name='investment_duration')
    amount_invested = models.DecimalField(decimal_places=2, max_digits=20, default=0)
    percentage = models.DecimalField(decimal_places=2, max_digits=20, default=0)
    return_on_invested = models.DecimalField(decimal_places=2, max_digits=20, default=0)
    number_of_month = models.IntegerField(default=1)
    number_of_days = models.IntegerField(default=1)
    status = models.CharField(max_length=100, choices=INVESTMENT_STATUS_CHOICES, default='pending')
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.pk}: {self.user}"




