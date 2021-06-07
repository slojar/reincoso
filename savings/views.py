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

        callback_url = request.data.get('callback_url')
        if not callback_url:
            callback_url = f"{request.scheme}://{request.get_host()}{request.path}"
        callback_url = callback_url + f"?gateway={gateway}"

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
                success = False
                response_status = status.HTTP_400_BAD_REQUEST
                json_response = None
                authorization_code = card.authorization_code
                paystack_auto_charge(authorization_code, email, amount, metadata=metadata)
                return success, json_response, response_status

            except Exception as ex:
                return Response({'success': False,
                                 'detail': 'Invalid card selected',
                                 'error': str(ex)},
                                status=status.HTTP_400_BAD_REQUEST)

        if gateway == 'paystack':
            success, response = get_paystack_link(email=email, amount=amount, callback_url=callback_url, metadata=metadata)
            if success:
                data['payment_link'] = response
            else:
                data['detail'] = response

        return Response(data)


class VerifyPaymentView(APIView):
    permission_classes = []

    def get(self, request):
        data = dict()
        gateway = request.GET.get('gateway')
        reference = request.GET.get('reference')
        phone_number = None

        if gateway == 'paystack':
            success, response = verify_paystack_transaction(reference)
            data['detail'] = response

            if success is False:
                return Response(data, status=status.HTTP_406_NOT_ACCEPTABLE)

            email = response['email']
            transaction_id = int(response['payload']['data']['metadata']['transaction_id'])

            profile = Profile.objects.get(user__email=email)
            phone_number = profile.phone_number

            payment_for = response['payload']['data']['metadata'].get('payment_for', None)

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

            # tokenize card
            tokenize_user_card(response)

        data['detail'] = "Transaction successful"
        data['msisdn'] = phone_number
        return Response(data)


