from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ugiinbichig.models import Marry
from ugiinbichig.serializers import MarrySerializers
from rest_framework.permissions import IsAuthenticated


class MarryView(APIView):
    permission_classes = [IsAuthenticated]

    # Бүх гэрлэлтийн бүртгэл эсвэл тодорхой нэгийг авах
    def get(self, request):
        human = request.query_params.get('human_id')

        if human:
            marry = Marry.objects.filter(human = human) | Marry.objects.filter(marryd=human)
            if not marry:
                return Response({"error": "Marry record not found"}, status=status.HTTP_404_NOT_FOUND)
            serializer = MarrySerializers(marry,many=True)
        else:
            marries = Marry.objects.all()
            serializer = MarrySerializers(marries, many=True)

        return Response({'status':'success', 'data':serializer.data}, status=status.HTTP_200_OK)

    # Гэрлэлт бүртгэх
    def post(self, request):
        serializer = MarrySerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status':'success'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Гэрлэлтийн бүртгэл шинэчлэх
    def put(self, request):
        marry_id = request.data.get('marry_ID')
        marry = Marry.objects.filter(marry_ID=marry_id).first()
        if not marry:
            return Response({"error": "Marry record not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = MarrySerializers(marry, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Гэрлэлтийн бүртгэл устгах
    def delete(self, request):
        marry_id = request.query_params.get('id')
        marry = Marry.objects.filter(marry_ID=marry_id).first()
        if not marry:
            return Response({"error": "Marry record not found"}, status=status.HTTP_404_NOT_FOUND)

        marry.delete()
        return Response({"message": "Marry record deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
