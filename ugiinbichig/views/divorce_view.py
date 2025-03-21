from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ugiinbichig.models import Divorce
from ugiinbichig.serializers import DivorceSerializers
from rest_framework.permissions import IsAuthenticated


class DivorceView(APIView):
    permission_classes = [IsAuthenticated]

    # Бүх салалтууд эсвэл тодорхой нэгийг авах
    def get(self, request):
        divorce_id = request.query_params.get('id')

        if divorce_id:
            divorce = Divorce.objects.filter(divorce_ID=divorce_id).first()
            if not divorce:
                return Response({"error": "Divorce record not found"}, status=status.HTTP_404_NOT_FOUND)
            serializer = DivorceSerializers(divorce)
        else:
            divorces = Divorce.objects.all()
            serializer = DivorceSerializers(divorces, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    # Салалт бүртгэх
    def post(self, request):
        serializer = DivorceSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Салалтын бүртгэл шинэчлэх
    def put(self, request):
        divorce_id = request.data.get('divorce_ID')
        divorce = Divorce.objects.filter(divorce_ID=divorce_id).first()
        if not divorce:
            return Response({"error": "Divorce record not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = DivorceSerializers(divorce, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Салалтын бүртгэл устгах
    def delete(self, request):
        divorce_id = request.query_params.get('id')
        divorce = Divorce.objects.filter(divorce_ID=divorce_id).first()
        if not divorce:
            return Response({"error": "Divorce record not found"}, status=status.HTTP_404_NOT_FOUND)

        divorce.delete()
        return Response({"message": "Divorce record deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
