import requests
from rest_framework import status
from rest_framework.authtoken.models import Token
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

    profile = Profile.objects.get(user__email=email)
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



