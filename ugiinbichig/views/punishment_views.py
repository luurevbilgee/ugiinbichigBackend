from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ugiinbichig.models.punishment_model import Punishment
from ugiinbichig.serializers import PunishmentSerializers
from rest_framework.permissions import IsAuthenticated


class PunishmentView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        human = request.query_params.get('human_ID') 
        
        if human:
            punishment = Punishment.objects.filter(human=human)
            if not punishment:
                return Response({"error": "Punishment record not found"}, status=status.HTTP_404_NOT_FOUND)
            serializer = PunishmentSerializers(punishment, many=True)

        return Response({'status': 'success', 'data': serializer.data}, status=status.HTTP_200_OK)


    # Нас баралтын бүртгэл үүсгэх
    def post(self, request):
        print(request.data)
        serializer =  PunishmentSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status':'success'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        # Extract punishment ID from URL parameters
        punishment_id =request.data.get('punishment_id')
        
        # Get the punishment instance, or return error if not found
        try:
            punishment = Punishment.objects.get(punishment_id=punishment_id)
        except Punishment.DoesNotExist:
            return Response({"error": "Punishment not found"}, status=status.HTTP_404_NOT_FOUND)
        
        # Pass the instance and the new data to the serializer
        serializer = PunishmentSerializers(punishment, data=request.data, partial=True)
        
        if serializer.is_valid():
            # Save the updated punishment data
            serializer.save()
            return Response({'status':'success', 'data':serializer.data},status=status.HTTP_201_CREATED)
        else:
            # If serializer data is invalid, return errors
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        punishment_id = request.query_params.get('id')  # "death_ID" биш, "id" гэж авах
        punishment = Punishment.objects.filter(punishment_id=punishment_id).first()

        if not punishment:
            return Response({"error": "Punishment record not found"}, status=status.HTTP_404_NOT_FOUND)

        punishment.delete()
        return Response({"message": "Punishment record deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
