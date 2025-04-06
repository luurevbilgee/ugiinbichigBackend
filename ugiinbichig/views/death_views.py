from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ugiinbichig.models.death_model import Death
from ugiinbichig.serializers import DeathSerializers
from rest_framework.permissions import IsAuthenticated


class DeathView(APIView):
    permission_classes = [IsAuthenticated]

    # Бүх нас баралтын бүртгэл эсвэл нэгийг авах
    def get(self, request):
        human = request.query_params.get('human_ID')

        if human:
            death = Death.objects.filter(human=human).first()
            if not death:
                return Response({"error": "Death record not found"}, status=status.HTTP_404_NOT_FOUND)
            serializer = DeathSerializers(death)

        return Response({'status':'success', 'data':serializer.data}, status=status.HTTP_200_OK)

    # Нас баралтын бүртгэл үүсгэх
    def post(self, request):
        serializer = DeathSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status':'success'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Нас баралтын бүртгэл шинэчлэх
    def put(self, request):
        death_id = request.data.get('death_ID')
        death = Death.objects.filter(death_ID=death_id).first()
        if not death:
            return Response({"error": "Death record not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = DeathSerializers(death, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Нас баралтын бүртгэл устгах
    def delete(self, request):
        death_id = request.query_params.get('id')
        death = Death.objects.filter(death_ID=death_id).first()
        if not death:
            return Response({"error": "Death record not found"}, status=status.HTTP_404_NOT_FOUND)

        death.delete()
        return Response({"message": "Death record deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
