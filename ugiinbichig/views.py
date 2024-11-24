from django.shortcuts import render
from .models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import LoginSerializer, UserSerializers, SignupSerializer
from django.contrib.auth.hashers import check_password
from django.db import IntegrityError
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
import logging
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
# Initialize a logger
logger = logging.getLogger(__name__)

class Login(APIView):
    def post(self, request):
        data = LoginSerializer(data=request.data)
        data.is_valid(raise_exception=True)

        email = data.validated_data['email']
        password = data.validated_data['password']
        
        try:
            user = User.objects.get(email=email)
            
            # Use check_password for secure password comparison
            if check_password(password, user.password):
                return Response("success", status=status.HTTP_200_OK)
            else:
                return Response("Нэвтрэх нэр эсвэл нууц үг буруу байна.", status=status.HTTP_401_UNAUTHORIZED)
        
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
                return Response("Хэрэглэгч бүртгэлтэй байна.", status=status.HTTP_400_BAD_REQUEST)  # HTTP_400_BAD_REQUEST is more appropriate
            else:
                # Use logging instead of print
                logger.info(f"Creating user: {username}")
                user = User(username=username, email=email, phone_number=phone_number)
                user.set_password(password)  # Correctly using set_password on the instance
                user.save()
                return Response("success", status=status.HTTP_201_CREATED)  # HTTP_201_CREATED indicates successful resource creation
            
        except IntegrityError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class CreateTokenView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')
        
        user = authenticate(username=email, password=password)

        if user :
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token)
            })
        else:
            return Response({'error': 'Нэвтрэх нэр болон нууц үг буруу байна'}, status=status.HTTP_401_UNAUTHORIZED)

class UserView(APIView):
    permission_classes = [IsAuthenticated]  # Ensure the request includes a valid token

    def get(self, request):
        try:
            # Access authenticated user
            user = request.user
            # Return user details or fetch additional data
            serializer = UserSerializers(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class CheckTokenView(APIView):
    permission_classes = [IsAuthenticated]  # Require a valid token

    def get(self, request):
        try:
            user = request.user
            print(request)
            return Response({
                'status': 'success',
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                }
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
