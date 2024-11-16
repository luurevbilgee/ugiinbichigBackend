from django.shortcuts import render
from . models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import LoginSerializer, UserSerializers, SignupSerializer
from django.contrib.auth.hashers import check_password
from django.db import IntegrityError
class Login (APIView):

    def post(self, request):
        data = LoginSerializer(data=request.data)
        data.is_valid(raise_exception=True)

        email = data.validated_data['email']
        password = data.validated_data['password']
       
        try:
            user = User.objects.get(email=email)
            print(user.password)
            if password == user.password:
                return Response("success", status=status.HTTP_200_OK)
            else:
                return Response("Нэвтрэх нэр эсвэл нууц үг буруу байна.", status=status.HTTP_404_NOT_FOUND)
        
        except User.DoesNotExist:
            return Response("Нэвтрэх нэр эсвэл нууц үг буруу байна.", status=status.HTTP_404_NOT_FOUND)

class Signup(APIView):
    def post(self, request):
        data = SignupSerializer(data=request.data)
        data.is_valid(raise_exception=True)
        username = data.validated_data["username"]
        email = data.validated_data["email"]
        phone_number = data.validated_data["phone_number"]
        password = data.validated_data["password"]
        try:
            if User.objects.filter(email=email).exists():
                return Response("Хэрэглэгч бүртгэлтэй байна.", status=status.HTTP_302_FOUND)
            else:
                print(username)
                user = User(username=username, email=email, phone_number=phone_number, password=password)
                user.save()
                return Response("success", status=status.HTTP_200_OK)
            
        except IntegrityError as e:
            return Response({"error": str(e)}, status=status.HTTP_302_FOUND)
