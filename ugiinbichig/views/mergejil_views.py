from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ugiinbichig.models import Mergejil
from ugiinbichig.serializers import MergejilSerializers
from rest_framework.permissions import IsAuthenticated

class MergejilView(APIView):
    permission_classes = [IsAuthenticated]

    # Бүх мэргэжил эсвэл тодорхой нэг мэргэжлийг авах
    def get(self, request):
        mergejil_id = request.query_params.get('id')
        human = request.query_params.get('human_id')
        if mergejil_id:
            mergejil = Mergejil.objects.filter(mergejil_ID=mergejil_id).first()
            if not mergejil:
                return Response({"error": "Mergejil not found"}, status=status.HTTP_404_NOT_FOUND)
            serializer = MergejilSerializers(mergejil)
        else:
            mergejils = Mergejil.objects.filter(human=human)
            serializer = MergejilSerializers(mergejils, many=True)
        
        return Response({'status':'success','data':serializer.data}, status=status.HTTP_200_OK)

    # Мэргэжил нэмэх
    def post(self, request):
        serializer = MergejilSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status':'success','data':serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Мэргэжил шинэчлэх
    def put(self, request):
        mergejil_ID = request.data.get('id')
        mergejil = Mergejil.objects.filter(mergejil_ID=mergejil_ID).first()
        if not mergejil:
            return Response({"error": "Mergejil not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = MergejilSerializers(mergejil, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'status':'success', 'data':serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Мэргэжил устгах
    def delete(self, request):
        mergejil_id = request.query_params.get('id')
        mergejil = Mergejil.objects.filter(mergejil_ID=mergejil_id).first()
        if not mergejil:
            return Response({"error": "Mergejil not found"}, status=status.HTTP_404_NOT_FOUND)

        mergejil.delete()
        return Response({'status': "success"}, status=status.HTTP_204_NO_CONTENT)
