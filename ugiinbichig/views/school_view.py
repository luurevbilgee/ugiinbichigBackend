from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ugiinbichig.models import School, Human,Shape
from ugiinbichig.serializers import SchoolSerializers
from rest_framework.permissions import IsAuthenticated

class SchoolView(APIView):
    permission_classes = [IsAuthenticated]

    # Бүх сургууль эсвэл тодорхой нэг сургуулийн мэдээллийг авах
    def get(self, request):
        human_id = request.query_params.get('human_ID')
        if human_id:
            school = School.objects.filter(human_id=human_id)
            if not school:
                return Response({"error": "School not found"}, status=status.HTTP_404_NOT_FOUND)
            serializer = SchoolSerializers(school, many=True)
        
        return Response({'data': serializer.data, 'status': 'success'}, status=status.HTTP_200_OK)

    # Сургууль нэмэх
    def post(self, request):
        human_id = request.query_params.get("human_ID")
        if human_id:
            # request data-д human ID-г нэмж байна
            data_with_human_id = request.data.copy()
            data_with_human_id['human'] = human_id
            # Serializer ашиглан хадгалалт хийх
            serializer = SchoolSerializers(data=data_with_human_id)
            if serializer.is_valid():
                serializer.save()
                return Response({'data':serializer.data, 'status': 'success'}, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "RD not found"}, status=status.HTTP_404_NOT_FOUND)
            # Сургууль шинэчлэх
    def put(self, request):
        school_id = request.data.get('school_ID')  # `id` зөв ирж байгаа эсэхийг шалгах
        if not school_id:
            return Response({"error": "ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        school = School.objects.filter(school_ID=school_id).first()
        if not school:
            return Response({"error": "School not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = SchoolSerializers(school, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'status': 'success', 'data': serializer.data}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Сургууль устгах
    def delete(self, request):
        school_id = request.query_params.get('id')
        school = School.objects.filter(school_ID=school_id).first()
        if not school:
            return Response({"error": "School not found"}, status=status.HTTP_404_NOT_FOUND)

        school.delete()
        return Response({"message": "School deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
