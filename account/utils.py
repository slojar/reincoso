import decimal

import requests
from django.db import transaction
import logging
import json
import base64
from django.db.models import Sum, Q
from rest_framework.authtoken.models import Token

from investment.models import UserInvestment
from investment.serializers import UserInvestmentSerializer
from loan.models import LoanTransaction, Loan
from loan.serializers import LoanSerializer
from savings.models import SavingTransaction, Saving
from savings.serializers import SavingSerializer
from .models import *
from django.contrib.auth.hashers import make_password
from django.conf import settings

from cryptography.fernet import Fernet

log = logging.getLogger(__name__)


def credit_user_account(profile, amount):
    profile.refresh_from_db()
    with transaction.atomic():
        wallet, new_wallet = Wallet.objects.select_for_update().get_or_create(user=profile)
        wallet.balance += decimal.Decimal(amount)
        wallet.save()
    profile.refresh_from_db()
    return profile


def debit_user_account(profile, amount):
    profile.refresh_from_db()
    with transaction.atomic():
        wallet, new_wallet = Wallet.objects.select_for_update().get_or_create(user=profile)
        wallet.balance -= decimal.Decimal(amount)
        wallet.save()
    profile.refresh_from_db()
    return profile


def encrypt_text(text: str):
    key = base64.urlsafe_b64encode(settings.SECRET_KEY.encode()[:32])
    fernet = Fernet(key)
    secure = fernet.encrypt(f"{text}".encode())
    return secure.decode()


def decrypt_text(text: str):
    key = base64.urlsafe_b64encode(settings.SECRET_KEY.encode()[:32])
    fernet = Fernet(key)
    decrypt = fernet.decrypt(text.encode())
    return decrypt.decode()


def reformat_phone_number(phone_number):
    return f"234{phone_number[-10:]}"


def signup(request):
    data = request.data
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    account_no = data.get('account_no')
    account_name = data.get('account_name')
    bank_name = data.get('bank_name')
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
    if not (account_no and account_name and bank_name):
        detail = 'Bank details are required'
        return success, detail
    if not (len(account_no) == 10 and str(account_no).isnumeric()):
        detail = 'Account number is not valid'
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
    user.first_name = first_name
    user.last_name = last_name
    user.email = email
    user.password = make_password(password)
    user.save()

    Token.objects.create(user=user)
    profile, created = Profile.objects.get_or_create(user=user)
    profile.phone_number = phone_number
    profile.bank_name = bank_name
    profile.account_name = account_name
    profile.bvn = encrypt_text(bvn)
    profile.account_no = encrypt_text(account_no)
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
    investment['total'] = UserInvestment.objects.filter(user=profile).count()
    investment['pending'] = UserInvestment.objects.filter(user=profile, status='pending').count()
    investment['approved'] = UserInvestment.objects.filter(user=profile, status='approved').count()
    investment['ongoing'] = UserInvestment.objects.filter(user=profile, status='ongoing').count()
    investment['completed'] = UserInvestment.objects.filter(user=profile, status='completed').count()
    investment['rejected'] = UserInvestment.objects.filter(user=profile, status='rejected').count()
    investment['cancelled'] = UserInvestment.objects.filter(user=profile, status='cancelled').count()
    investment['failed'] = UserInvestment.objects.filter(user=profile, status='failed').count()

    query = Q(status='approved') | Q(status='ongoing') | Q(status='completed')
    total_money_invested = UserInvestment.objects.filter(user=profile).filter(query)
    investment['total_money_invested'] = total_money_invested.aggregate(Sum('amount_invested'))['amount_invested__sum']

    query = Q(status='ongoing')
    total_money_expected = UserInvestment.objects.filter(user=profile).filter(query)
    investment['total_money_expected'] = total_money_expected.aggregate(Sum('return_on_invested'))['return_on_invested__sum'] or 0

    current = UserInvestment.objects.filter(user=profile, status='ongoing')
    investment['current_investments'] = UserInvestmentSerializer(current, many=True).data

    data['savings'] = savings
    data['investment'] = investment
    data['loan'] = loan

    return data



