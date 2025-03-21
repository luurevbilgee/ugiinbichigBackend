from django.shortcuts import render
from ugiinbichig.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
import logging

from django.core.mail import send_mail
import random
from django.core.cache import cache
logger = logging.getLogger(__name__)

class OPT(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        action = request.data.get('action')
        email = request.data.get('email')
        
       
        if not email:
            return Response({'error': "Имэйл оруулна уу"},status=400)
        
        if action == 'forget':
            user = User.objects.filter(email=email).exists()
            if not user :
                return Response({"error": "Бүртгэлгүй имэйл байна"})
            opt = random.randint(100000,999999)
            cache.set(email, opt, timeout=300)
            
            # Имэйл илгээх 
            
            send_mail(
                subject='Таны баталгаажуулах код',
                message=f'Таны баталгаажуулах код: {opt}',
                from_email='luurevbilgee@yahoo.com',
                recipient_list=[email],
                fail_silently= False,
            )
            return Response({'message': "Баталгаажуулах код амжилттай илгээгдлээ", 'status': 'success'}, status=200)
        
        if action == 'send':
            opt = random.randint(100000,999999)
            cache.set(email, opt, timeout=300)
            
            # Имэйл илгээх 
            
            send_mail(
                subject='Таны баталгаажуулах код',
                message=f'Таны баталгаажуулах код: {opt}',
                from_email='luurevbilgee@yahoo.com',
                recipient_list=[email],
                fail_silently= False,
            )
            return Response({'message': "Баталгаажуулах код амжилттай илгээгдлээ", 'status': 'success'}, status=200)
    
        elif action =='verify':
            opt = request.data.get('opt')
            
            if not opt:
                return Response({'error': "Баталгаажуулах код буруу байна"}, status=400)
            
            cached_opt = cache.get(email)
            
            if cached_opt and str(cached_opt) == opt:
                return Response({"message":'Баталгаажуулалт амжилттай', 'status':'success'},status=200)
            return Response({'error':' Код буруу байна эсвэл баталгаажуулах кодны хугацаа дууссан байна.'},status= 400)
        
        else:
            return Response({'error': "Зөвшөөрөгдөөгүй хүсэлт"}, status=400)