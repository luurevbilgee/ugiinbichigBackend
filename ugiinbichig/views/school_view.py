from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ugiinbichig.models import School
from ugiinbichig.serializers import SchoolSerializer
from rest_framework.permissions import IsAuthenticated

class SchoolView(APIView):
    permission_classes = [IsAuthenticated]

    # Бүх сургууль эсвэл тодорхой нэг сургуулийн мэдээллийг авах
    def get(self, request):
        school_id = request.query_params.get('id')

        if school_id:
            school = School.objects.filter(school_ID=school_id).first()
            if not school:
                return Response({"error": "School not found"}, status=status.HTTP_404_NOT_FOUND)
            serializer = SchoolSerializer(school)
        else:
            schools = School.objects.all()
            serializer = SchoolSerializer(schools, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)

    # Сургууль нэмэх
    def post(self, request):
        serializer = SchoolSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Сургууль шинэчлэх
    def put(self, request):
        school_id = request.data.get('school_ID')
        school = School.objects.filter(school_ID=school_id).first()
        if not school:
            return Response({"error": "School not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = SchoolSerializer(school, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Сургууль устгах
    def delete(self, request):
        school_id = request.query_params.get('id')
        school = School.objects.filter(school_ID=school_id).first()
        if not school:
            return Response({"error": "School not found"}, status=status.HTTP_404_NOT_FOUND)

        school.delete()
        return Response({"message": "School deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
