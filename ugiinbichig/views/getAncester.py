from django.http import JsonResponse
from ugiinbichig.models.getAncestorsInfo import get_ancestors_info
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
class AncestorsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        human_id =int( request.query_params.get("human_id"))
        max_level=int( request.query_params.get('max_level'))
        ancestors_info = get_ancestors_info(human_id, max_level)
        if ancestors_info:
            return Response({'status':'success', 'data':ancestors_info}, status=status.HTTP_202_ACCEPTED)
        else:
            return JsonResponse({"error": "Мэдээлэл олдсонгүй"}, status=404)
