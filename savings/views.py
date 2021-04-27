from datetime import datetime, timedelta
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from bot.utils import get_paystack_link
from savings.models import Duration, Saving
from transaction.models import SavingTransaction


class SavingsView(APIView):
    def post(self, request):
        data = dict()
        amount = request.data.get('amount')
        fixed_payment = request.data.get('fixed_payment')
        repayment_day = request.data.get('repayment_day')
        gateway = request.data.get('gateway')
        callback_url = request.data.get('callback_url')
        payment_duration_id = request.data.get('payment_duration_id')

        if not Duration.objects.filter(id=payment_duration_id).exists():
            data['detail'] = 'Invalid payment duration'
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

        email = request.user.email
        payment_duration_id = Duration.objects.get(id=payment_duration_id)

        if not callback_url:
            callback_url = f"{request.scheme}://{request.get_host()}{request.path}"
        callback_url = callback_url + f"?gateway={gateway}"

        if fixed_payment:
            amount = fixed_payment

        # Create/Update Saving Account
        saving, created = Saving.objects.get_or_create(user=request.user.profile)
        saving.duration = payment_duration_id
        saving.last_payment = amount
        saving.amount = fixed_payment
        saving.last_payment_date = datetime.now()
        saving.total_savings = saving.total_savings + amount
        saving.repayment_day = repayment_day

        # Calculate next repayment date
        last_date = saving.last_payment_date
        duration_interval = saving.duration.interval
        next_date = last_date + timedelta(days=duration_interval)
        saving.next_payment_date = next_date
        saving.save()

        # Create saving transaction
        transaction, created = SavingTransaction.objects.get_or_create(user=request.user.profile,
                                                                       saving_id=saving.id, status='pending')
        transaction.payment_method = gateway
        transaction.amount = amount
        transaction.save()

        if gateway == 'paystack':
            metadata = {
                "transaction_id": transaction.id,
            }
            success, response = get_paystack_link(email=email, amount=amount, callback_url=callback_url,
                                                  metadata=metadata)
            if success:
                data['payment_link'] = response
            else:
                data['detail'] = response

        return Response(data)

