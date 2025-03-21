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
                user = request.user

                # Human обьектийг шалгах
                human = Human.objects.get(user_ID_id=user.id)

                # Шинэ зураг хадгалах
                setImage = Image.objects.create(
                    human_id=human.human_ID,
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
            user = request.user
            import os
            print(os.path.join(settings.MEDIA_ROOT, 'image', 'download_z2fzqzk.png'))
            # Human-ийг шалгах
            human = Human.objects.get(user_ID_id=user.id)

            # Human-д холбогдсон зургуудыг авах
            images = Image.objects.filter(human_id=human.human_ID)
            if not images.exists():
                return Response({
                    'error': 'No images found for this user.'
                }, status=status.HTTP_404_NOT_FOUND)

            # Сүүлчийн зургийг авах
            latest_image = images.last()
            full_image_url = f"{settings.MEDIA_URL}{latest_image.image}"

            # Амжилттай хариу буцаах
            return Response({
                'status': 'success',
                'data': {
                    'image': full_image_url,
                    'description': latest_image.discription
                }
            }, status=status.HTTP_200_OK)

        except Human.DoesNotExist:
            return Response({
                'error': 'Human profile not found for this user.'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                'error': str(e),
                'details': 'Something went wrong while fetching the image.'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
