from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.core.cache import cache
from django.contrib.auth.hashers import make_password

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework_jwt.settings import api_settings

from apps.staff.models import StaffProfile, Role
import datetime
# Create your views here.


class Login(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
            jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

            payload = jwt_payload_handler(user)
            token = jwt_encode_handler(payload)

            try:
                role = Role.objects.get(user=user).tipe
            except Exception as _:
                role = "-"

            msg = {
                'role': role,
                'token': token
            }

            return Response(msg, status=status.HTTP_200_OK)
        else:
            return Response({"msg": "username atau password salah"}, status=status.HTTP_400_BAD_REQUEST)


class SignupStaff(APIView):

    permission_classes = (AllowAny,)

    def post(self, request):
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        nik = request.data.get('nik')
        email = request.data.get('email', None)
        kontak = request.data.get('kontak', None)
        contract_date = request.data.get('contract_date')
        bod = request.data.get('bod')
        role = request.data.get('role')
        user_name = request.data.get('username')
        password = request.data.get('password')

        role_dict = {
            "MANAGEMENT": 1,
            "RESEPSIONIS": 2,
            "ROOM_SERVICE": 3,
            "CHEF": 4,
            "SECURITY": 5,
        }

        try:
            kontrak_date = datetime.datetime.strptime(
                contract_date, "%Y-%m-%d")
            bod = datetime.datetime.strptime(bod, "%Y-%m-%d")
            hashed_password = make_password(password)
            User.objects.create(username=user_name, password=hashed_password)
            obj = User.objects.get(username=user_name)
            Role.objects.create(user=obj, tipe=role_dict[role])
            StaffProfile.objects.create(
                full_name=first_name+" "+last_name, nik=nik, email=email, kontak=kontak, bod=bod, contract_date=kontrak_date, user=obj)
            return Response({"message": "OK"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
