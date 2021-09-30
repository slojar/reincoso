from threading import Thread

from django.db.models import Q
from django.utils import timezone

from account.models import UserCard
from account.utils import tokenize_user_card
from modules.paystack import paystack_auto_charge, generate_payment_ref_with_paystack, verify_paystack_transaction
from savings.models import Saving
from savings.utils import create_savings_transaction, update_savings_payment, process_savings_payment_with_card


def auto_save_cron():

    now = timezone.datetime.today()
    this_day = now.day
    this_month = now.month
    this_time = now.time()

    query = Q(auto_save=True)
    query = query & Q(next_payment_date__month=this_month)
    query = query & Q(next_payment_date__day__lte=this_day)
    query = query & Q(next_payment_date__hour__lte=this_time.hour)

    exclude = Q(last_payment_date__month=this_month, last_payment_date__day__lte=this_day)

    for saving in Saving.objects.filter(query).filter().exclude(exclude):
        success = False
        amount = saving.amount
        user = saving.user.user
        user_profile = saving.user
        gateway = saving.payment_gateway
        try:
            card = UserCard.objects.get(user=user_profile, gateway=gateway, default=True)
        except Exception as ex:
            card = UserCard.objects.filter(user=user_profile, gateway=gateway).last()

        if not card:
            saving.status = 'failed'
            saving.save()
            # notify user of card unavailability via email

        if card:
            process_savings_payment_with_card(saving=saving, card=card, amount=amount)


# print(auto_save_cron())


