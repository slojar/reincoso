import requests
from django.db.models import Sum, Q
from rest_framework import status
from rest_framework.authtoken.models import Token

from investment.models import Investment
from investment.serializers import InvestmentSerializer
from loan.models import LoanTransaction, Loan
from loan.serializers import LoanSerializer
from savings.models import SavingTransaction, Saving
from savings.serializers import SavingSerializer
from .models import *
from django.contrib.auth.hashers import make_password
from django.conf import settings
import logging
import json

log = logging.getLogger(__name__)


def reformat_phone_number(phone_number):
    return f"234{phone_number[-10:]}"


def signup(request):
    data = request.data
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    email = data.get('email')
    phone_number = data.get('phone_number')
    bvn = data.get('bvn')
    gender = data.get('gender')
    success = False

    if not email:
        detail = 'Email address not provided'
        return success, detail
    if User.objects.filter(email=email).exists():
        detail = 'Email already exist'
        return success, detail
    if not phone_number:
        detail = 'Phone number not provided'
        return success, detail
    else:
        phone_number = reformat_phone_number(phone_number)
    if User.objects.filter(username=phone_number).exists():
        detail = 'Phone number taken'
        return success, detail
    if not bvn:
        detail = 'BVN number not provided'
        return success, detail
    if Profile.objects.filter(bvn=bvn).exists():
        detail = 'Another user has registered with this BVN'
        return success, detail

    password = phone_number
    user, created = User.objects.get_or_create(username=phone_number)
    if created:
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.password = make_password(password)
        user.save()

    Token.objects.create(user=user)
    profile, created = Profile.objects.get_or_create(user=user)
    if created:
        profile.phone_number = phone_number
        profile.bvn = bvn
        profile.gender = gender
        profile.save()

    success = True
    detail = 'Account created successfully'
    return success, detail


def tokenize_user_card(data, gateway=None):
    if not data:
        return False
    data = data['payload']
    authorization = data['data']['authorization']
    email = data['data']['customer']['email']
    bank = authorization['bank']
    card_type = authorization['card_type']
    bin_ = authorization['bin']
    last4 = authorization['last4']
    exp_month = authorization['exp_month']
    exp_year = authorization['exp_year']
    signature = authorization['signature']
    authorization_code = authorization['authorization_code']
    name = authorization.get('account_name')

    profile = Profile.objects.get(user__email__iexact=email)
    card, created = UserCard.objects.get_or_create(user=profile, email=email, bank=bank, signature=signature)
    card.name = name
    card.gateway = gateway or 'paystack'
    card.card_type = str(card_type).strip()
    card.bin = bin_
    card.last4 = last4
    card.exp_month = exp_month
    card.exp_year = exp_year
    card.last4 = last4
    card.authorization_code = authorization_code
    card.payload = authorization
    card.save()

    if UserCard.objects.filter(user=profile).count() <= 1:
        UserCard.objects.filter(user=profile).update(default=True)


def get_user_analytics(profile):
    data = dict()

    savings = dict()
    total_savings = SavingTransaction.objects.filter(user=profile, status='success')
    savings['total_savings_amount'] = total_savings.aggregate(Sum('amount'))['amount__sum']
    savings['current_saving'] = SavingSerializer(Saving.objects.filter(user=profile).last()).data

    loan = dict()
    loan_transactions = LoanTransaction.objects.filter(user=profile, status='success')
    loan['loan_transaction_amount'] = loan_transactions.aggregate(Sum('amount'))['amount__sum']
    loan['current_loans'] = LoanSerializer(Loan.objects.filter(user=profile, status='ongoing'), many=True).data
    loan['total'] = Loan.objects.filter(user=profile).count()
    loan['pending'] = Loan.objects.filter(user=profile, status='pending').count()
    loan['processing'] = Loan.objects.filter(user=profile, status='processing').count()
    loan['approved'] = Loan.objects.filter(user=profile, status='approved').count()
    loan['unapproved'] = Loan.objects.filter(user=profile, status='unapproved').count()
    loan['awaiting guarantor feedback'] = Loan.objects.filter(user=profile, status='awaiting guarantor feedback').count()
    loan['ongoing'] = Loan.objects.filter(user=profile, status='ongoing').count()
    loan['repaid'] = Loan.objects.filter(user=profile, status='repaid').count()

    investment = dict()
    investment['total'] = Investment.objects.filter(user=profile).count()
    investment['pending'] = Investment.objects.filter(user=profile, status='pending').count()
    investment['approved'] = Investment.objects.filter(user=profile, status='approved').count()
    investment['ongoing'] = Investment.objects.filter(user=profile, status='ongoing').count()
    investment['completed'] = Investment.objects.filter(user=profile, status='completed').count()
    investment['rejected'] = Investment.objects.filter(user=profile, status='rejected').count()
    investment['cancelled'] = Investment.objects.filter(user=profile, status='cancelled').count()
    investment['failed'] = Investment.objects.filter(user=profile, status='failed').count()

    query = Q(status='approved') | Q(status='ongoing') | Q(status='completed')
    total_money_invested = Investment.objects.filter(user=profile).filter(query)
    investment['total_money_invested'] = total_money_invested.aggregate(Sum('amount_invested'))['amount_invested__sum']

    query = Q(status='ongoing')
    total_money_expected = Investment.objects.filter(user=profile).filter(query)
    investment['total_money_expected'] = total_money_expected.aggregate(Sum('return_on_invested'))['return_on_invested__sum'] or 0

    current = Investment.objects.filter(user=profile, status='ongoing')
    investment['current_investments'] = InvestmentSerializer(current, many=True).data

    data['savings'] = savings
    data['investment'] = investment
    data['loan'] = loan

    return data



