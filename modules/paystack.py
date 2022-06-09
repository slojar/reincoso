import json
import uuid
import requests
import logging

from django.conf import settings
from rest_framework import status

from account.models import Bank

log = logging.getLogger(__name__)


def verify_paystack_transaction(reference):
    success = True
    message = ''
    if not reference:
        success = False
        message = 'Sorry, we could not verify your payment at the moment, please try again.'
        return success, message

    url = settings.PAYSTACK_BASE_URL + f"/transaction/verify/{reference}"
    headers = {
        'Authorization': 'Bearer {}'.format(settings.PAYSTACK_SECRET_KEY),
    }
    response = requests.get(url, headers=headers)
    json_response = response.json()

    log.info(f"url: {url}")
    log.info(f"headers: {headers}")
    log.info(f"response: {response.text}")

    if json_response.get('status') is not True:
        success = False
        message = json_response.get('message')

    if success is True:
        if json_response['data']['status'] != 'success':
            success = False
        else:
            success = True
        message = {
            'email': json_response['data']['customer']['email'],
            'transaction_id': reference,
            'transaction_status': json_response.get('data').get('status'),
            'amount': float(json_response.get('data').get('amount')) / 100,
            'payload': json_response
        }
    return success, message


def paystack_auto_charge(authorization_code, email, amount, **kwargs):
    success = False
    url = settings.PAYSTACK_BASE_URL + "/transaction/charge_authorization"
    amount = round(float(amount))

    reference = kwargs.get('reference')
    metadata = kwargs.get("metadata")

    payload = dict()
    payload['authorization_code'] = authorization_code
    payload['email'] = email
    payload['authorization_code'] = authorization_code
    payload['amount'] = f"{amount}00"
    payload['metadata'] = kwargs.get("metadata")
    if reference:
        payload['reference'] = reference
    if metadata:
        if kwargs.get('metadata').get("reference"):
            payload['reference'] = kwargs.get('metadata').get("reference")

    payload = json.dumps(payload)
    headers = {
        'Authorization': 'Bearer {}'.format(settings.PAYSTACK_SECRET_KEY),
        'Content-Type': 'application/json'
    }
    response = requests.post(url, headers=headers, data=payload)
    json_response = response.json()

    log.info(f"url: {url}")
    log.info(f"headers: {headers}")
    log.info(f"payload: {payload}")
    log.info(f"response: {response.text}")

    try:
        if json_response.get("status") is True:
            if json_response['data']['status'] == 'success':
                success = True
    except Exception as ex:
        log.error(f"An error occurred on auto-debit: {ex}")
    return success, json_response


def get_paystack_link(email, amount, callback_url=None, metadata=None, **kwargs):
    # metadata = kwargs.get('metadata')
    # callback_url = kwargs.get('callback_url')
    callback_url = callback_url + f"?gateway=paystack"
    currency = kwargs.get('currency')
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
    if metadata:
        if metadata.get("reference"):
            payload['reference'] = metadata.get("reference")

    payload = json.dumps(payload)
    headers = {
        'Authorization': 'Bearer {}'.format(settings.PAYSTACK_SECRET_KEY),
    }
    response = requests.post(url, headers=headers, data=payload)
    json_response = response.json()

    print("Payload to PAYSTACK", payload)

    log.info(f"url: {url}")
    log.info(f"headers: {headers}")
    log.info(f"payloads: {payload}")
    log.info(f"response: {response.text}")

    if json_response.get('status') is True:
        response = json_response['data']['authorization_url']
    else:
        success = False
        response = json_response
        if json_response.get('message'):
            response = json_response.get('message')
    return success, response


def generate_payment_ref_with_paystack(uid):
    if not settings.PAYSTACK_REF:
        settings.PAYSTACK_REF = "COSO"
    return f'{uid}-{settings.PAYSTACK_REF}-{uuid.uuid4()}'


def get_banks():
    url = settings.PAYSTACK_BASE_URL + "/bank"
    data = {"country": "nigeria"}
    response = requests.get(url, params=data).json()
    data = response['data']
    for institution in data:
        bank, _ = Bank.objects.get_or_create(code=institution['code'])
        bank.name = institution['name']
        bank.save()
    return response


def validate_account_no(account_no, bank_code):
    url = settings.PAYSTACK_BASE_URL + "/bank/resolve"
    header = {'Authorization': f'Bearer {settings.PAYSTACK_SECRET_KEY}'}
    data = {"account_number": account_no, "bank_code": bank_code}
    response = requests.get(url, params=data, headers=header).json()
    log.info(f"url: {url}")
    log.info(f"header: {header}")
    log.info(f"payloads: {data}")
    log.info(f"response: {response}")
    return response


def create_recipient_code(profile, account_no):
    url = settings.PAYSTACK_BASE_URL + "/transferrecipient"
    header = {'Authorization': f'Bearer {settings.PAYSTACK_SECRET_KEY}'}
    data = {
        "account_number": account_no,
        "bank_code": profile.bank.code,
        "type": "nuban",
        "name": profile.account_name,
        "currency": "NGN"
    }
    response = requests.post(url, data=data, headers=header).json()
    log.info(f"url: {url}")
    log.info(f"header: {header}")
    log.info(f"payloads: {data}")
    log.info(f"response: {response}")

    if response['status'] is True:
        code = response['data']['recipient_code']
        profile.recipient_code = code
        profile.save()
    return True


def initialize_transfer(recipient_code, description, amount):
    url = settings.PAYSTACK_BASE_URL + "/transfer"
    header = {"Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}"}
    payload = {
        "source": "balance",
        "reason": description,
        "amount": amount,
        "recipient": recipient_code,
    }
    response = requests.post(url, data=payload, headers=header).json()
    log.info(f"url: {url}")
    log.info(f"header: {header}")
    log.info(f"payloads: {payload}")
    log.info(f"response: {response}")
    return response


def finalize_transfer(transfer_code, code):
    url = settings.PAYSTACK_BASE_URL + "/transfer/finalize_transfer"
    header = {"Content-Type": "application/json", "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}"}
    payloads = {
        "transfer_code": transfer_code,
        "otp": code,
    }
    response = requests.post(url, data=payloads, headers=header).json()
    log.info(f"url: {url}")
    log.info(f"header: {header}")
    log.info(f"payloads: {payloads}")
    log.info(f"response: {response}")
    return response




