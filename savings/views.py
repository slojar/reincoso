import logging
from datetime import datetime, timedelta
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from savings.models import Duration, Saving, SavingTransaction
from .serializers import *
from settings.models import PaymentGateway
from modules.paystack import verify_paystack_transaction
from modules.paystack import get_paystack_link
from account.utils import tokenize_user_card
from account.models import UserCard
from modules.paystack import paystack_auto_charge
from transaction.models import Transaction
from investment.utils import approve_investment


class SavingsView(APIView):
    def get(self, request):
        data = dict()
        queryset = Duration.objects.all()
        data['durations'] = SavingDurationSerializer(queryset, many=True).data
        data['gateways'] = PaymentGateway.objects.all().values('id', 'name', 'slug')
        return Response(data)

    def post(self, request):
        data = dict()
        amount = request.data.get('amount')
        fixed_payment = request.data.get('fixed_payment')
        repayment_day = request.data.get('repayment_day')
        gateway = request.data.get('gateway')
        payment_duration_id = request.data.get('payment_duration_id')
        card_id = request.data.get('card_id')

        if not Duration.objects.filter(id=payment_duration_id).exists():
            data['detail'] = 'Invalid payment duration'
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

        email = request.user.email
        payment_duration_id = Duration.objects.get(id=payment_duration_id)

        if fixed_payment:
            amount = fixed_payment

        # Create/Update Saving Account
        saving, created = Saving.objects.get_or_create(user=request.user.profile)
        saving.title = payment_duration_id
        saving.last_payment = amount

        if not fixed_payment:
            saving.amount = amount

        if saving.amount <= 0 and fixed_payment:
            saving.amount = fixed_payment

        saving.last_payment_date = datetime.now()
        saving.total = saving.total + amount
        saving.repayment_day = repayment_day

        # Calculate next repayment date
        last_date = saving.last_payment_date
        duration_interval = saving.title.interval
        next_date = last_date + timedelta(days=duration_interval)
        saving.next_payment_date = next_date
        saving.save()

        # Create saving transaction
        transaction, created = SavingTransaction.objects.get_or_create(user=request.user.profile,
                                                                       saving_id=saving.id, status='pending')
        transaction.payment_method = gateway
        transaction.amount = amount
        transaction.save()

        metadata = {
            'transaction_id': transaction.id,
            'payment_for': 'savings',
        }

        if card_id:
            try:
                card = UserCard.objects.get(id=card_id)
                authorization_code = card.authorization_code
                success, response = paystack_auto_charge(authorization_code, email, amount, metadata=metadata)
                if not success:
                    data['detail'] = "There is an error in request sent"
                    data['data'] = response
                    return Response(data, status.HTTP_400_BAD_REQUEST)

                reference = response['data']['reference']

                success, response = verify_paystack_transaction(reference)
                if not success:
                    data['detail'] = "There is an error in request sent"
                    data['data'] = response
                    return Response(data, status.HTTP_400_BAD_REQUEST)

                transaction.reference = reference
                transaction.status = 'success'
                transaction.response = response
                transaction.save()

                data['detail'] = "Payment successful"
                return Response(data)

            except Exception as ex:
                logging.exception(f"{ex}")
                data = {
                    'success': False,
                    'detail': 'Invalid card selected',
                    'error': str(ex)
                }
                return Response(data, status=status.HTTP_400_BAD_REQUEST)

        if not card_id:
            callback_url = request.data.get('callback_url')
            if not callback_url:
                callback_url = f"{request.scheme}://{request.get_host()}{request.path}"

            if gateway == 'paystack':
                success, response = get_paystack_link(email=email, amount=amount, callback_url=callback_url, metadata=metadata)
                if success:
                    data['payment_link'] = response
                else:
                    data['detail'] = response
            return Response(data)

        return Response(data)


class VerifyPaymentView(APIView):
    permission_classes = []

    def get(self, request):
        data = dict()
        gateway = request.GET.get('gateway')
        reference = request.GET.get('reference')
        phone_number = None
        success = False
        response = dict()

        if gateway == 'paystack':
            success, response = verify_paystack_transaction(reference)
            data['detail'] = response

            if success is False:
                return Response(data, status=status.HTTP_406_NOT_ACCEPTABLE)

            email = response['email']
            transaction_id = response['payload']['data']['metadata'].get('transaction_id', None)
            payment_for = response['payload']['data']['metadata'].get('payment_for', None)
            profile = Profile.objects.get(user__email__iexact=email)
            phone_number = profile.phone_number

            if payment_for == 'membership fee':
                trans = Transaction.objects.get(id=transaction_id, transaction_type=payment_for)
                trans.reference = reference
                trans.status = 'success'
                trans.response = response
                trans.save()

            if payment_for == 'savings':
                trans = SavingTransaction.objects.get(id=transaction_id, user__user__email__iexact=email)
                trans.reference = reference
                trans.status = 'success'
                trans.response = response
                trans.save()

            if payment_for == 'investment':
                investment_id = response['payload']['data']['metadata'].get('investment_id', None)
                success, response = approve_investment(investment_id, gateway, reference)
                data['detail'] = response
                if success is False:
                    return Response(data, status.HTTP_400_BAD_REQUEST)
                return Response(data)

            # tokenize card
            tokenize_user_card(response, gateway)

        if success is False:
            data['detail'] = "Transaction could not be verified at the moment"
        else:
            data['detail'] = "Transaction successful"
        data['msisdn'] = phone_number
        return Response(data)


