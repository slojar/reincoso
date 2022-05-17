import logging
from .models import Loan, LoanTransaction
from account.models import UserCard
from django.utils import timezone
from modules.paystack import paystack_auto_charge
from .utils import verify_loan_repayment

log = logging.getLogger(__name__)


def loan_repayment_cron():
    loans = Loan.objects.filter(status='ongoing')
    for loan in loans:
        transactions = LoanTransaction.objects.filter(loan=loan, transaction_type='repayment', status='success').count()
        if transactions < loan.basis_duration:
            this_month = timezone.now().month
            this_date = timezone.now().day
            this_day = timezone.now().isoweekday()
            this_time = int(f"{timezone.now().hour}{timezone.now().minute}")
            month_to_pay = loan.next_repayment_date.month
            day_to_pay = loan.day_of_the_week
            date_to_pay = loan.next_repayment_date.day
            time_to_pay = int(f"{loan.next_repayment_date.hour}{loan.next_repayment_date.minute}")

            if loan.basis == 'weekly':
                repay = this_month == month_to_pay and this_day == int(day_to_pay) and this_time >= time_to_pay
            if loan.payment_day != '30' and loan.basis != 'weekly':
                date_to_pay = int(loan.payment_day)
                repay = this_month == month_to_pay and this_date == date_to_pay and this_time >= time_to_pay

            repay = this_month == month_to_pay and this_date == date_to_pay and this_time >= time_to_pay

            if repay is True:
                print("Auto debit user card")

                profile = loan.user
                amount = loan.amount_to_repay_split

                transaction, _ = LoanTransaction.objects.get_or_create(
                    user=profile, loan=loan, transaction_type='repayment', amount=amount, status='pending'
                )

                metadata = {
                    'payment_type': 'loan_repayment',
                    'loan_id': loan.id,
                    'transaction_id': transaction.id,
                }

                user_card_id = UserCard.objects.filter(user=profile).last()

                # Charge user's card automatically
                authorization_code = user_card_id.authorization_code
                email = profile.user.email

                success, response = paystack_auto_charge(authorization_code=authorization_code, email=email,
                                                         amount=amount, metadata=metadata)

                log.info(f'Auto_Deduct_Loan_CRON: Charging user card --->>> success: {success}')
                log.info(f'Auto_Deduct_Loan_CRON: Charging user card --->>> response: {response}')

                if success is False:
                    return success, response.get('message')

                reference = response['data']['reference']
                success, response = verify_loan_repayment(user_card_id.gateway, reference)

                log.info(f'Auto_Deduct_Loan_CRON: Verifying payment --->>> success: {success}')
                log.info(f'Auto_Deduct_Loan_CRON: Verifying payment --->>> response: {response}')

                # notify user for transaction and auto-debit of loan payment

