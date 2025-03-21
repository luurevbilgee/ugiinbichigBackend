from django.shortcuts import render
from ugiinbichig.models import  Human
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ugiinbichig.serializers import HumanSaveSerializers
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated


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