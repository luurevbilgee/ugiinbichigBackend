from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ugiinbichig.models import ProfilePicture, Human
from ugiinbichig.serializers import ProfilePictureSerializer

class ProfilePictureView(APIView):

    def get(self, request):
        # human_ID параметрийг авах
        human_id = request.query_params.get("human_ID")
        
        if human_id:
            try:
                # human_ID ашиглан ProfilePicture авах
                profile_picture = ProfilePicture.objects.get(human_id=human_id)
                serializer = ProfilePictureSerializer(profile_picture)
                return Response({'status': 'success', 'data': serializer.data}, status=status.HTTP_200_OK)
            except ProfilePicture.DoesNotExist:
                return Response({"error": "Profile picture not found."}, status=status.HTTP_404_NOT_FOUND)
        
        # Хэрвээ human_ID байхгүй бол, одоогийн хэрэглэгчийн зураг авах
        user_id = request.user.id
        human = Human.objects.filter(user_ID=user_id).first()
        
        if not human:
            return Response({"error": "Human not found."}, status=status.HTTP_404_NOT_FOUND)

        try:
            profile_picture = ProfilePicture.objects.get(human_id=human.human_ID)
            serializer = ProfilePictureSerializer(profile_picture)
            return Response({'status': 'success', 'data': serializer.data}, status=status.HTTP_200_OK)
        except ProfilePicture.DoesNotExist:
            return Response({"error": "Profile picture not found."}, status=status.HTTP_404_NOT_FOUND)



    def post(self, request):
        human = request.query_params.get("human_ID")
        
        # Хэрвээ human_ID байхгүй бол зураг болон тайлбар авах
        if not human:
            image = request.FILES.get('image')
            description = request.data.get('description', "")
            
            if not image:
                return Response({"error": "Image is required."}, status=status.HTTP_400_BAD_REQUEST)

            user = request.user
            human = Human.objects.filter(user_ID=user).first()

            # Хэрэглэгчийн профайл зураг байвал шинэчилнэ
            profile_picture, created = ProfilePicture.objects.update_or_create(
                human=human,  # human объект ашиглаж байна
                defaults={'image': image, 'description': description},
            )
            serializer = ProfilePictureSerializer(profile_picture)
            return Response({'status': 'success', 'data': serializer.data, "id": profile_picture.profile}, status=status.HTTP_201_CREATED)

        # human_ID байх тохиолдолд, human параметрийг request-д нэмэх
        data = request.data.copy()
        data["human"] = human  # human_ID-ийг request data-д нэмэх

        # Шинээр өгөгдлийг сериализ хийх
        serializer = ProfilePictureSerializer(data=data)  # serializer болон өгөгдөлөө

        if serializer.is_valid():
            # Хэрэв сериализаци амжилттай бол
            return Response({'status': 'success', 'data': serializer.data, "id":serializer.profile}, status=status.HTTP_201_CREATED)

        # Хэрвээ алдаа гарсан бол
        return Response({"error": "Invalid data."}, status=status.HTTP_400_BAD_REQUEST)
