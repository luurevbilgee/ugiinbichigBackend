from django.http import JsonResponse
from ugiinbichig.models.getHumanDetails import get_human_details
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
class HumanDetails(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        human_id =int( request.query_params.get("human_id"))
        human_info = get_human_details(human_id)
        if human_info:
            return Response({'status':'success', 'data':human_info}, status=status.HTTP_202_ACCEPTED)
        else:
            return JsonResponse({"error": "Мэдээлэл олдсонгүй"}, status=404)
