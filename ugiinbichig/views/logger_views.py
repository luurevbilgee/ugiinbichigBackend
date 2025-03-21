from django.shortcuts import render
from ugiinbichig.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ugiinbichig.serializers import LoginSerializer, SignupSerializer
from django.contrib.auth.hashers import check_password
from django.db import IntegrityError
from rest_framework.permissions import AllowAny
import logging

logger = logging.getLogger(__name__) 

class Login(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        # Serializer-ийг шалгах
        data = LoginSerializer(data=request.data)
        data.is_valid(raise_exception=True)

        email = data.validated_data['email']
        password = data.validated_data['password']
        
        try:
            user = User.objects.get(email=email)

            # Нууц үгийг шалгах
            if check_password(password, user.password):
                logger.info(f"Нэвтэрсэн хэрэглэгч: {email}")
                return Response({"message": "Амжилттай нэвтэрлээ"}, status=status.HTTP_200_OK)
            else:
                logger.warning(f"Нууц үг буруу: {email}")
                return Response({"error": "Нэвтрэх нэр эсвэл нууц үг буруу байна."}, status=status.HTTP_401_UNAUTHORIZED)
        
        except User.DoesNotExist:
            logger.error(f"Хэрэглэгч олдсонгүй: {email}")
            return Response({"error": "Нэвтрэх нэр эсвэл нууц үг буруу байна."}, status=status.HTTP_404_NOT_FOUND)


class Signup(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        # Serializer-ийг шалгах
        data = SignupSerializer(data=request.data)
        data.is_valid(raise_exception=True)

        username = data.validated_data["username"]
        email = data.validated_data["email"]
        phone_number = data.validated_data["phone_number"]
        password = data.validated_data["password"]
        
        try:
            # И-мэйл бүртгэгдсэн эсэхийг шалгах
            if User.objects.filter(email=email).exists():
                logger.warning(f"Бүртгэлтэй имэйл байна: {email}")
                return Response({"error": "Бүртгэлтэй имэйл байна."}, status=status.HTTP_208_ALREADY_REPORTED)

            # Хэрэглэгч үүсгэх
            user = User(username=username, email=email, phone_number=phone_number)
            user.set_password(password)  # Нууц үгийг шифрлэж хадгална
            user.save()
            logger.info(f"Хэрэглэгч амжилттай бүртгэгдлээ: {username} ({email})")

            return Response({"message": "Амжилттай бүртгэгдлээ"}, status=status.HTTP_201_CREATED)
        
        except IntegrityError:
            logger.error(f"Бүртгэлтэй утасны дугаар байна: {phone_number}")
            return Response({"error": "Бүртгэлтэй утасны дугаар байна."}, status=status.HTTP_208_ALREADY_REPORTED)
