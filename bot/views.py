from rest_framework.response import Response
from rest_framework.views import APIView
from .utils import *
from django.contrib.auth import authenticate


class SignupView(APIView):
    permission_classes = []

    def post(self, request):
        data = dict()
        success, detail, response = signup(request)
        data['success'] = success
        data['detail'] = detail
        return Response(data, status=response)


class LoginView(APIView):
    permission_classes = []

    def post(self, request):
        phone_number = request.data.get('phone_number')
        password = request.data.get('password')

        data = dict()
        data['success'] = False
        if not phone_number:
            data['detail'] = 'Phone number not provided'
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        else:
            phone_number = f"234{phone_number[-10:]}"
        if not User.objects.filter(username=phone_number).exists():
            data['detail'] = 'Account with this phone number does not exist'
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=phone_number, password=password)

        token = Token.objects.get(user__username=phone_number)
        token.delete()
        token = Token.objects.create(user=user)

        if not user:
            data['detail'] = 'Incorrect phone number or password'
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

        data['success'] = True
        data['detail'] = 'Login successful'
        data['token'] = token.key
        return Response(data, status=status.HTTP_200_OK)




