from django.shortcuts import render
from .models import User, Human,Image, Shape
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
        print(urgiin_ovog, ovog, ys_undes, name, RD, birth_date, birth_year, birth_counter, gender)
        try:
            user = request.user
            id = User.objects.get(id = user.id)
            human = Human(user_ID = id ,urgiin_ovog = urgiin_ovog, ovog = ovog, ys_undes = ys_undes, name = name, RD = RD, birth_date= birth_date , birth_counter = birth_counter, birth_year= birth_year, gender = gender)
            human.save()
            return Response({
                'status': 'success',
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
            user = request.user
            id = User.objects.get(id = user.id)
            human = Human(user_ID = id ,urgiin_ovog = urgiin_ovog, ovog = ovog, ys_undes = ys_undes, name = name, RD = RD, birth_date= birth_date , birth_counter = birth_counter, birth_year= birth_year, gender = gender)
            human.save()
            return Response({
                'status': 'success',
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
        try:
            shapes = Shape.objects.all()

            if not shapes:
                return Response({
                    'error': 'No shapes found for this user.','data':'null'
                })

            shape = ShapeSerializer(shapes, many=True)

            if len(shape.data) == 0:
                return Response({
                    'error': 'No images found for this user.'
                }, status=status.HTTP_404_NOT_FOUND)

            return Response({'status': 'success', 'data': shape.data}, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"Error fetching shapes for user {request.user.id}: {str(e)}")
            return Response({
                'error': str(e),
                'details': 'Something went wrong while retrieving the shape.'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def post(self, request):
        print("Received data:", request.data)  # Log the incoming data
        shapes_data = request.data  # Directly access request.data as it is already a list
        print(shapes_data)
        
        if not shapes_data:
            return Response({"error": "Shape data is required"}, status=status.HTTP_400_BAD_REQUEST)

        # Human ID-г shape мэдээлэлд нэмэх
        for shape_data in shapes_data:
            serializer = ShapeSerializer(data=shape_data)
            print(serializer)
            if serializer.is_valid():
                serializer.save()  # Shape хадгалах
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # Алдаа гарсан тохиолдолд

        return Response({"status": "success"}, status=status.HTTP_201_CREATED)  # Хариу амжилттай хадгалагдсан бол
