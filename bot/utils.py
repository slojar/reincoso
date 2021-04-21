from rest_framework import status
from rest_framework.authtoken.models import Token
from .models import *
from django.contrib.auth.hashers import make_password


def signup(request):
    data = request.data
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    email = data.get('email')
    password = data.get('password')
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
    if not password:
        detail = 'Password not provided'
        return success, detail, response
    if len(password) < 8:
        detail = 'Password length should be 8 or more characters'
        return success, detail, response

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


