from django.shortcuts import render
from .models import User, Human,Image, Shape ,Who
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import LoginSerializer, UserSerializers, SignupSerializer, HumanSaveSerializers, HumanSerializers, ImageSerializers, ShapeSerializer
from django.contrib.auth.hashers import check_password
from django.db import IntegrityError
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
import logging
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError


# opt код илгээх болон баталгаажуулах 
from django.core.mail import send_mail
# from django.http import JsonResponse
import random
from django.core.cache import cache
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
    permission_classes = [AllowAny]
    def post(self, request):
        data = SignupSerializer(data=request.data)
        data.is_valid(raise_exception=True)
        username = data.validated_data["username"]
        email = data.validated_data["email"]
        phone_number = data.validated_data["phone_number"]
        password = data.validated_data["password"]
        print(email)
        try:
            if User.objects.filter(email=email).exists():
                return Response({'error':"Бүртгэлтэй имэйл  байна."},status=status.HTTP_208_ALREADY_REPORTED)  
            else:
                # Use logging instead of print
                logger.info(f"Creating user: {username}")
                user = User(username=username, email=email, phone_number=phone_number)
                user.set_password(password)  # Correctly using set_password on the instance
                user.save()
                return Response("success", status=status.HTTP_201_CREATED)  # HTTP_201_CREATED indicates successful resource creation
            
        except IntegrityError as e:
            return Response({"error": 'Бүртгэлтэй утасны дугаар байна'}, status=status.HTTP_208_ALREADY_REPORTED)

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
            return Response({'status' : 'success','data': serializer.data}, status=status.HTTP_200_OK)
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
                }
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UserNamtarView(APIView):
    permission_classes = [IsAuthenticated] 
    def post(self, request):
        data = HumanSaveSerializers(data=request.data)
        data.is_valid(raise_exception=True)
        urgiin_ovog = data.validated_data["urgiin_ovog"]
        ovog = data.validated_data["ovog"]
        ys_undes = data.validated_data["ys_undes"]
        name = data.validated_data["name"]
        RD = data.validated_data["RD"]
        birth_date = data.validated_data["birth_date"]
        birth_counter = data.validated_data["birth_year"]
        birth_year = data.validated_data["birth_year"]
        gender = data.validated_data["gender"]
        try:
            user = request.user
            id = User.objects.get(id = user.id)
            human = Human(user_ID = id ,urgiin_ovog = urgiin_ovog, ovog = ovog, ys_undes = ys_undes, name = name, RD = RD, birth_date= birth_date , birth_counter = birth_counter, birth_year= birth_year, gender = gender)
            human.save()
            return Response({
                'status': 'success',
                'data': human.human_ID,
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
    def get(self, request):
        try:
            user = request.user  # Request-аас одоогийн хэрэглэгчийг авна
            humans = Human.objects.filter(user_ID_id=user.id)  # Шүүлт хийх
            if not humans.exists():  # Хоосон эсэхийг шалгах
                return Response({
                    "status": "fail",
                    "message": "No related Human records found for the user."
                }, status=status.HTTP_404_NOT_FOUND)

            # Хэрэв шүүлтийн үр дүн олдвол амжилтын хариу өгөх
            return Response({
                "status": "success",
                "data": HumanSaveSerializers(humans, many=True).data # Жишээ нь: обьектыг dict болгох
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def put(self, request):
        try:
            user = request.user  # Одоогийн хэрэглэгчийг авна
            humans = Human.objects.filter(user_ID_id=user.id)  

            if not humans.exists():  # Хоосон эсэхийг шалгах
                return Response({
                    "status": "fail",
                    "message": "No related Human records found for the user."
                }, status=status.HTTP_404_NOT_FOUND)

            # Оруулсан өгөгдлийг авах
            data = request.data

            # Бичлэг бүрийг шинэчлэнэ
            for human in humans:
                for key, value in data.items():
                    setattr(human, key, value)  # Өгөгдлийг шинэчилнэ
                human.save()  # Бичлэг хадгалах

            return Response({
                "status": "success",
                "message": "Records updated successfully."
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class HumanView(APIView):
    permission_classes = [IsAuthenticated] 

   
    def post(self, request):
        data = HumanSaveSerializers(data=request.data)
        data.is_valid(raise_exception=True)
        urgiin_ovog = data.validated_data["urgiin_ovog"]
        ovog = data.validated_data["ovog"]
        ys_undes = data.validated_data["ys_undes"]
        name = data.validated_data["name"]
        RD = data.validated_data["RD"]
        birth_date = data.validated_data["birth_date"]
        birth_counter = data.validated_data["birth_year"]
        birth_year = data.validated_data["birth_year"]
        gender = data.validated_data["gender"]
        print(urgiin_ovog, ovog, ys_undes, name, RD, birth_date, birth_year, birth_counter, gender)
        try:
            human = Human(urgiin_ovog = urgiin_ovog, ovog = ovog, ys_undes = ys_undes, name = name, RD = RD, birth_date= birth_date , birth_counter = birth_counter, birth_year= birth_year, gender = gender)
            human.save()
            return Response({
                'status': 'success',
                'data': human.human_ID,
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
              
    def get(self, request):
        try:
            human_ID = request.query_params.get('id')
            print(human_ID)
            if not human_ID:  # Хоосон эсэхийг шалгах
                return Response({
                    "status": "fail",
                    "message": "human_ID параметр шаардлагатай."
                }, status=status.HTTP_400_BAD_REQUEST)

            humans = Human.objects.filter(human_ID=human_ID)  # Шүүлт хийх

            if not humans:  # QuerySet хоосон эсэхийг шалгах
                return Response({
                    "status": "fail",
                    "message": "No related Human records found for the user."
                }, status=status.HTTP_404_NOT_FOUND)

            return Response({
                "status": "success",
                "data": HumanSaveSerializers(humans, many=True).data
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                "status": "error",
                "message": "Internal server error",
                "details": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        
    def put(self, request):
        try:
            user = request.user  # Одоогийн хэрэглэгчийг авна
            humans = Human.objects.filter(user_ID_id=user.id)  

            if not humans.exists():  # Хоосон эсэхийг шалгах
                return Response({
                    "status": "fail",
                    "message": "No related Human records found for the user."
                }, status=status.HTTP_404_NOT_FOUND)

            # Оруулсан өгөгдлийг авах
            data = request.data

            # Бичлэг бүрийг шинэчлэнэ
            for human in humans:
                for key, value in data.items():
                    setattr(human, key, value)  # Өгөгдлийг шинэчилнэ
                human.save()  # Бичлэг хадгалах

            return Response({
                "status": "success",
                "message": "Records updated successfully."
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


   
class UserImage(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = ImageSerializers(data=request.data) 
        if data.is_valid():
            try:
                user = request.user
                
                try:
                    human = Human.objects.get(user_ID_id=user.id)
                except Human.DoesNotExist:
                    return Response({
                        'error': 'Human profile not found for this user.'
                    }, status=status.HTTP_404_NOT_FOUND)

                setImage = Image.objects.create(
                    human_id=human.human_ID,
                    image=data.validated_data['image'],  
                    discription=data.validated_data['discription']
                )
                setImage.save()
                return Response({
                    'status': 'success',
                }, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({
                    'error': str(e),
                    'details': 'Something went wrong while saving the image.'
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            print("Invalid data:", data.errors)
            return Response(data.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def get(self, request):
            try:
                user = request.user
                
                try:
                    human = Human.objects.get(user_ID_id=user.id)
                except Human.DoesNotExist:
                    return Response({
                        'error': 'Human profile not found for this user.'
                    }, status=status.HTTP_404_NOT_FOUND)

                images = Image.objects.filter(human_id = human.human_ID)
                if not images:
                    return Response({
                        'error': 'No images found for this user.'
                    }, status=status.HTTP_404_NOT_FOUND)
                image = ImageSerializers(images, many=True)
                print(len(image.data) )
                if len(image.data) == 0:
                    return Response({
                        'error': 'No images found for this user.'
                    }, status=status.HTTP_404_NOT_FOUND)
                return Response({'status':'success','data':image.data[-1]}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({
                    'error': str(e),
                    'details': 'Something went wrong while saving the image.'
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ShapeList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        shape_id = request.query_params.get("shapeID")
        try:
            if not shape_id:  # shape_id байхгүй эсвэл хоосон бол
                shapes = Shape.objects.all()
                
                if not shapes.exists():
                    return Response({
                        'status': 'error',
                        'message': 'Дүрс олдсонгүй',
                        'data': None
                    }, status=status.HTTP_404_NOT_FOUND)

                # ✅ ShapeSerializer-д `many=True` тохиргоотой serialize хийх
                shape_data = ShapeSerializer(shapes, many=True).data

                return Response({
                    'status': 'success',
                    'data': shape_data
                }, status=status.HTTP_200_OK)

            else:
                shape = Shape.objects.filter(shape_id=shape_id).first()

                if not shape:
                    return Response({
                        'status': 'error',
                        'message': 'Дүрс олдсонгүй',
                        'data': None
                    }, status=status.HTTP_404_NOT_FOUND)

                shape_data = ShapeSerializer(shape).data

                return Response({
                    'status': 'success',
                    'data': shape_data
                }, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"Error fetching shape {shape_id}: {str(e)}")
            return Response({
                'status': 'error',
                'message': 'Internal server error',
                'details': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        shape_data = request.data
        try:
            human_ID = shape_data.get("human_ID")
            existing_shape = Shape.objects.filter(human_ID=human_ID).first()
            if existing_shape and existing_shape.human:
                return Response({
                    "status": "error",
                    "message": f"Shape {human_ID} already has a human assigned."
                }, status=status.HTTP_400_BAD_REQUEST)

            serializer = ShapeSerializer(data=shape_data)
            if serializer.is_valid():
                serializer.save()
            else:
                return Response({
                    "status": "error",
                    "message": "Invalid data",
                    "errors": serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)

            return Response({
                "status": "success",
                "message": "Shapes created successfully"
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            logger.error(f"Error creating shapes: {str(e)}")
            return Response({
                "status": "error",
                "message": "Internal server error",
                "details": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, shape_id):
        try:
            shape = Shape.objects.filter(shape_id=shape_id).first()
            if not shape:
                return Response({
                    "status": "error",
                    "message": "Shape not found"
                }, status=status.HTTP_404_NOT_FOUND)

            # Хэрэв shape-д холбогдсон human байгаа эсэхийг шалгах
            if shape.human:
                return Response({
                    "status": "error",
                    "message": f"Shape {shape_id} already has a human assigned."
                }, status=status.HTTP_400_BAD_REQUEST)

            serializer = ShapeSerializer(shape, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    "status": "success",
                    "data": serializer.data
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    "status": "error",
                    "message": "Хүчингүй өгөгдөл",
                    "errors": serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            logger.error(f"Error updating shape {shape_id}: {str(e)}")
            return Response({
                "status": "error",
                "message": "Дотоод серверийн алдаа",
                "details": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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
class ResetPassword(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        new_password = request.data.get("newPassword")

        if not email or not new_password:
            return Response({"error": "Имэйл болон нууц үг шаардлагатай."})

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error": "Имэйл бүртгэлгүй байна."})

        user.set_password(new_password)
        user.save()
        return Response({"status": "success", "message": "Нууц үг амжилттай шинэчлэгдлээ."})
    
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Who, User  # Загвараа зөв импортлоорой

class Relation(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        human_ID = request.data.get("human_ID")
        relation_ID = request.data.get("relation_ID")
        nershil = request.data.get("nershil")

        try:
            relation = Who.objects.create(human_id=human_ID, relations_id=relation_ID, lavlah=nershil)
            return Response({
                'status': 'success',
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
