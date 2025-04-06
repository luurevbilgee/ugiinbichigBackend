from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from ugiinbichig.models import Who, Human
from ugiinbichig.serializers import WhoSerializer

class Relation(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # QueryDict бол dict хувилбарыг үүсгэнэ
            # Шинэ түлхүүр нэмнэ
        data= request.data
        print(data)
        serializer = WhoSerializer(data=data)
        if serializer.is_valid():
            human_ID = serializer.validated_data["human"]
            relation_ID = serializer.validated_data["relations"]

            # Давхардал шалгах
            if Who.objects.filter(human_id=human_ID, relations_id=relation_ID).exists():
                return Response({"error": "Relation already exists."}, status=status.HTTP_400_BAD_REQUEST)

            serializer.save()
            return Response({"status": "success"}, status=status.HTTP_201_CREATED)
    
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        human_ID = request.query_params.get("human_ID")

        if human_ID:
            relations = Who.objects.filter(human=human_ID) | Who.objects.filter(relations=human_ID)
            
            if not relations.exists():
                return Response({"error": "No relations found for this human ID."}, status=status.HTTP_404_NOT_FOUND)

        serializer = WhoSerializer(relations, many=True)
        return Response({'status': 'success', 'data': serializer.data}, status=status.HTTP_200_OK)
