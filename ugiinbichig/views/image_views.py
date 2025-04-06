from django.shortcuts import render
from ugiinbichig.models import  Human,Image
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ugiinbichig.serializers import ImageSerializers
from rest_framework.permissions import IsAuthenticated

from django.conf import settings

 
class UserImage(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = ImageSerializers(data=request.data) 
        if data.is_valid():
            try:
                human = request.query_params.get('humanID')
                # Шинэ зураг хадгалах
                setImage = Image.objects.create(
                    human_id=human,
                    image=data.validated_data['image'],
                    discription=data.validated_data['discription']
                )
                setImage.save()
                
                # Бүрэн замыг буцаах
                full_image_url = f"{settings.MEDIA_URL}{setImage.image}"
                return Response({
                    'status': 'success',
                    'image_url': full_image_url
                }, status=status.HTTP_200_OK)

            except Human.DoesNotExist:
                return Response({
                    'error': 'Human profile not found for this user.'
                }, status=status.HTTP_404_NOT_FOUND)
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
            human_ID = request.query_params.get("human_ID")
            # human_ID орж ирсэн эсэхийг шалгах
            if not human_ID:
                return Response({"error": "human_ID is required."}, status=status.HTTP_400_BAD_REQUEST)

            # Human-ийг хайх
            try:
                human = Human.objects.get(human_ID=human_ID)
            except Human.DoesNotExist:
                return Response({"error": "Human not found."}, status=status.HTTP_404_NOT_FOUND)

            # Human-д холбогдсон бүх зургуудыг авах
            images = Image.objects.filter(human=human)
            if not images.exists():
                return Response({
                    'error': 'No images found for this human.'
                }, status=status.HTTP_404_NOT_FOUND)

            # Зургийг сериализация хийх
            serialized_images = ImageSerializers(images, many=True).data
            return Response({
                'status': 'success',
                'data': serialized_images
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    def delete(self, request):
            image = request.query_params.get('id')
            images = Image.objects.filter(img_ID=image).first()
            print(images)
            if not images:
                return Response({"error": "images record not found"}, status=status.HTTP_404_NOT_FOUND)

            images.delete()
            return Response({"message": "Health record deleted successfully"}, status=status.HTTP_204_NO_CONTENT)