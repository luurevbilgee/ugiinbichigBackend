from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ugiinbichig.models import ProfilePicture, Human
from ugiinbichig.serializers import ProfilePictureSerializer

class ProfilePictureView(APIView):

    def get(self, request):
        # human_ID параметрийг авах
        human_id = request.query_params.get("humanID")
        print(human_id)
        if human_id:
            try:
                # human_ID ашиглан ProfilePicture авах
                profile_picture = ProfilePicture.objects.get(human_id=human_id)
                serializer = ProfilePictureSerializer(profile_picture)
                return Response({'status': 'success', 'data': serializer.data}, status=status.HTTP_200_OK)
            except ProfilePicture.DoesNotExist:
                return Response({"error": "Profile picture not found."}, status=status.HTTP_404_NOT_FOUND)
        
        # Хэрвээ human_ID байхгүй бол, одоогийн хэрэглэгчийн зураг авах
        if not human_id:
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
        return Response({"error": "Profile picture not found."}, status=status.HTTP_404_NOT_FOUND)


    def post(self, request):
        human_id = request.query_params.get("humanID")  # humanID-г query параметрээс авна

        # Хэрвээ human_ID байхгүй бол зураг болон тайлбар авах
        if not human_id:
            image = request.FILES.get('image')  # Image-ийг FILES-ээс авах
            description = request.data.get('description', "")  # Тайлагдал авна

            # Хэрвээ зураг байхгүй бол алдаа өгнө
            if not image:
                return Response({"error": "Image is required."}, status=status.HTTP_400_BAD_REQUEST)

            user = request.user.id  # Одоогийн хэрэглэгчийн ID-ийг авах
            human = Human.objects.filter(user_ID=user).first()  # human объектыг авах

            if not human:
                return Response({"error": "Human not found."}, status=status.HTTP_404_NOT_FOUND)

            # Хэрэглэгчийн профайл зураг байвал шинэчилнэ
            profile_picture, created = ProfilePicture.objects.update_or_create(
                human=human,  # human объект ашиглаж байна
                defaults={'image': image, 'description': description},
            )

            # ProfilePictureSerializer ашиглан сериализ хийх
            serializer = ProfilePictureSerializer(profile_picture)
            return Response({'status': 'success', 'data': serializer.data}, status=status.HTTP_201_CREATED)

        # Хэрвээ human_ID байх тохиолдолд, human параметрийг request-д нэмэх
        if human_id:
            data = request.data.copy()
            image = request.FILES.get('image')  # image-ийг data-д нэмэх
            description = request.data.get('description', '')  # description-ийг data-д нэмэх

            # Хэрвээ зураг байхгүй бол алдаа өгнө
            if not image:
                return Response({"error": "Image is required."}, status=status.HTTP_400_BAD_REQUEST)

            # human_ID-ийг ашиглан human объект олох
            try:
                human = Human.objects.get(human_ID=human_id)  # human объектыг авах
            except Human.DoesNotExist:
                return Response({"error": "Human not found."}, status=status.HTTP_404_NOT_FOUND)

            # Хэрвээ data-д image болон description байгаа бол сериализац хийх
            profile_picture, created = ProfilePicture.objects.update_or_create(
                human=human,  # human объект ашиглаж байна
                defaults={'image': image, 'description': description},
            )

            serializer = ProfilePictureSerializer(profile_picture)
            
            return Response({'status': 'success', 'data': serializer.data}, status=status.HTTP_201_CREATED)

        # Хэрвээ алдаа гарсан бол
        return Response({"error": "Invalid data."}, status=status.HTTP_400_BAD_REQUEST)
