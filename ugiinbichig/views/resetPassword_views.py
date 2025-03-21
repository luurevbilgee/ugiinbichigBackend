from django.shortcuts import render
from ugiinbichig.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

class ResetPassword(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email", "").strip()
        new_password = request.data.get("newPassword", "").strip()

        # Шалгалтууд
        if not email or not new_password:
            return Response(
                {"error": "Имэйл болон нууц үг шаардлагатай."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {"error": "Имэйл бүртгэлгүй байна."},
                status=status.HTTP_404_NOT_FOUND
            )

        # Нууц үг шинэчлэх
        user.set_password(new_password)
        user.save()

        return Response(
            {"status": "success", "message": "Нууц үг амжилттай шинэчлэгдлээ."},
            status=status.HTTP_200_OK
        )
