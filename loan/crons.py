from .models import Loan, LoanTransaction
from django.utils import timezone


# def loan_repayment_cron():
#     loans = Loan.objects.filter(status='ongoing')
#     for loan in loans:
#         transactions = LoanTransaction.objects.filter(loan=loan, transaction_type='repayment', status='success').count()
#         if transactions < loan.basis_duration:
#             this_month = timezone.now().month
#             this_day = timezone.now().day
#             this_time = int(f"{timezone.now().hour}{timezone.now().minute}")
#             month_to_pay = loan.next_repayment_date.month
#             day_to_pay = loan.next_repayment_date.day
#             time_to_pay = int(f"{loan.next_repayment_date.hour}{loan.next_repayment_date.minute}")
#
#             repay = this_month == month_to_pay and this_day == day_to_pay and this_time >= time_to_pay
#
#             if repay is True:
#                 print("Auto debit user card")
#                 # Charge user's card automatically
#                 # update last repayment date field to now
#                 # update next repayment date field to next payment
#                 # update amount repaid
#                 # create transaction for user
#                 # notify user for transaction and auto-debit of loan payment
#
#
#
# loan_repayment_cron()





