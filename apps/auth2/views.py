from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.core.cache import cache
from django.contrib.auth.hashers import make_password
from django.db.models import Q
from django.core.cache import cache

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework_jwt.settings import api_settings

from apps.staff.models import StaffProfile, Role
from apps.reservation.models import Guest
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

            is_staff = user.is_staff

            msg = {
                'role': role,
                'token': token,
                'staff': is_staff
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
            User.objects.create(username=user_name,
                                password=hashed_password, is_staff=True)
            obj = User.objects.get(username=user_name)
            Role.objects.create(user=obj, tipe=role_dict[role])
            StaffProfile.objects.create(
                full_name=first_name+" "+last_name, nik=nik, email=email, kontak=kontak, bod=bod, contract_date=kontrak_date, user=obj)
            return Response({"message": "OK"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class Signup(APIView):

    permission_classes = (AllowAny,)

    def post(self, request):
        first_name = request.data.get("first_name")
        last_name = request.data.get('last_name')
        nip = request.data.get('nip')
        kontak = request.data.get('kontak', None)
        email = request.data.get('email')
        username = request.data.get('username')
        password = request.data.get('password')

        try:
            hashed_password = make_password(password)
            obj = User.objects.filter(username=username)
            if len(obj) != 0:
                return Response({"message": "Username sudah ada"})
            obj = Guest.objects.filter(Q(nip=nip) | Q(email=email))
            if len(obj) != 0:
                return Response({"message": "Anda sudah terdaftar"})

            User.objects.create(username=username,
                                password=hashed_password, is_staff=False)
            obj = User.objects.get(username=username)
            Guest.objects.create(nama=first_name+" "+last_name,
                                 nip=nip, kontak=kontak, email=email, user=obj)
            return Response({"message": "OK"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):

    # permission_classes = (IsTokenValid,)
    permission_classes = (AllowAny,)
    authentication_classes = []

    def post(self, request):

        http_status = 200
        request_status = "OK"

        try:
            token = request.META['HTTP_AUTHORIZATION']

            if "JWT " in token:
                token = token.replace("JWT ", "")
                cache.set(('token-%s' % token), token, timeout=1200)

        except Exception as e:
            pass

        return Response({"status": request_status, "message": "Logout success"}, status=http_status)
