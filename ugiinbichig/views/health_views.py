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
        human_id = request.query_params.get('human_id')
        if health_id:
            health = Health.objects.filter(health_ID=health_id).first()
            if not health:
                return Response({"error": "Health record not found"}, status=status.HTTP_404_NOT_FOUND)
            serializer = HealthSerializers(health)
            return Response({'status':'success','data':serializer.data}, status=status.HTTP_200_OK)
        if human_id:
            health = Health.objects.filter(human_id=human_id)
            if not health:
                return Response({"error": "Health record not found"}, status=status.HTTP_404_NOT_FOUND)
            serializer = HealthSerializers(health, many=True)

            return Response({'status':'success','data':serializer.data}, status=status.HTTP_200_OK)
        return Response({"error": "Health record not found"}, status=status.HTTP_404_NOT_FOUND)

    # Эрүүл мэндийн бүртгэл нэмэх
    def post(self, request):
        serializer = HealthSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status':'success'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Эрүүл мэндийн бүртгэл шинэчлэх
    def put(self, request):
        health_id = request.data.get('health_ID')
        print(health_id)
        health = Health.objects.filter(health_ID=health_id).first()
        if not health:
            return Response({"error": "Health record not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = HealthSerializers(health, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'status':'success','data':serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Эрүүл мэндийн бүртгэл устгах
    def delete(self, request):
        health_id = request.query_params.get('id')
        health = Health.objects.filter(health_ID=health_id).first()
        if not health:
            return Response({"error": "Health record not found"}, status=status.HTTP_404_NOT_FOUND)

        health.delete()
        return Response({"message": "Health record deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
