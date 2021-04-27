import requests
from rest_framework import status
from rest_framework.authtoken.models import Token
from .models import *
from django.contrib.auth.hashers import make_password
from django.conf import settings
import logging
import json

log = logging.getLogger(__name__)


def signup(request):
    data = request.data
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    email = data.get('email')
    phone_number = data.get('phone_number')
    bvn = data.get('bvn')
    gender = data.get('gender')

    success = False
    response = status.HTTP_400_BAD_REQUEST

    if not email:
        detail = 'Email address not provided'
        return success, detail, response
    if User.objects.filter(email=email).exists():
        detail = 'Email already exist'
        return success, detail, response
    if not phone_number:
        detail = 'Phone number not provided'
        return success, detail, response
    else:
        phone_number = f"234{phone_number[-10:]}"
    if User.objects.filter(username=phone_number).exists():
        detail = 'Phone number taken'
        return success, detail, response
    if not bvn:
        detail = 'BVN number not provided'
        return success, detail, response
    if Profile.objects.filter(bvn=bvn).exists():
        detail = 'Another user has registered with this BVN'
        return success, detail, response

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
    response = status.HTTP_201_CREATED

    return success, detail, response


def get_paystack_link(email, amount, **kwargs):
    metadata = kwargs.get('metadata')
    currency = kwargs.get('currency')
    callback_url = kwargs.get('callback_url')
    url = settings.PAYSTACK_BASE_URL + "/transaction/initialize"
    success = True
    amount = round(float(amount))
    payload = {
        "email": email,
        "amount": f"{amount}00",
        "callback_url": callback_url,
        "currency": currency,
        "metadata": metadata
    }
    payload = json.dumps(payload)
    headers = {
        'Authorization': 'Bearer {}'.format(settings.PAYSTACK_SECRET_KEY),
    }
    response = requests.post(url, headers=headers, data=payload)
    json_response = response.json()

    log.info(f"url: {url}")
    log.info(f"headers: {headers}")
    log.info(f"payloads: {payload}")
    log.info(f"response: {response.text}")

    if json_response.get('status') is True:
        response = json_response['data']['authorization_url']
    else:
        success = False
        response = json_response

    return success, response


