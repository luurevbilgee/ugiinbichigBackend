from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ugiinbichig.models import Health
from ugiinbichig.serializers import HealthSerializers
from rest_framework.permissions import IsAuthenticated

class HealthView(APIView):
    permission_classes = [IsAuthenticated]

    # Бүх эрүүл мэндийн бүртгэл эсвэл тодорхой нэгийг авах
    def get(self, request):
        health_id = request.query_params.get('id')

        if health_id:
            health = Health.objects.filter(health_ID=health_id).first()
            if not health:
                return Response({"error": "Health record not found"}, status=status.HTTP_404_NOT_FOUND)
            serializer = HealthSerializers(health)
        else:
            healths = Health.objects.all()
            serializer = HealthSerializers(healths, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    # Эрүүл мэндийн бүртгэл нэмэх
    def post(self, request):
        serializer = HealthSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Эрүүл мэндийн бүртгэл шинэчлэх
    def put(self, request):
        health_id = request.data.get('health_ID')
        health = Health.objects.filter(health_ID=health_id).first()
        if not health:
            return Response({"error": "Health record not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = HealthSerializers(health, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Эрүүл мэндийн бүртгэл устгах
    def delete(self, request):
        health_id = request.query_params.get('id')
        health = Health.objects.filter(health_ID=health_id).first()
        if not health:
            return Response({"error": "Health record not found"}, status=status.HTTP_404_NOT_FOUND)

        health.delete()
        return Response({"message": "Health record deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
