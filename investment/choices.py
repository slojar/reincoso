INVESTMENT_SPEC_CHOICES = (
    ('key metric', "Key metric"),
    ('minimum return', "Minimum return"),
    ('target for return per annum', "Target for return per annum"),
    ('investible asset claim', "Investible asset claim"),
    ('30 days average return', "30 days average return"),
    ('return on investment', "Return on investment"),
    ('minimum investment', "Minimum investment"),
    ('maximum investment', "Maximum investment"),
)

AVAILABLE_INVESTMENT_STATUS_CHOICES = (
    ('active', 'Active'), ('inactive', 'Inactive'),
)

TRANSACTION_TYPE_CHOICES = (
    ('investment', 'Investment'),
)

basis_type_choices = (
    ('weekly', 'Weekly'), ('monthly', 'Monthly'), ('yearly', 'Yearly'),
)

INVESTMENT_STATUS_CHOICES = (
    ('pending', 'Pending'), ('approved', 'Approved'), ('ongoing', 'Ongoing'), ('completed', 'Completed'),
    ('rejected', 'Rejected'), ('cancelled', 'Cancelled'), ('failed', 'Failed'),
)

TRANSACTION_STATUS_CHOICES = (
    ('pending', 'Pending'), ('unsuccessful', 'Unsuccessful'), ('cancelled', 'Cancelled'), ('success', 'Success'),
)

