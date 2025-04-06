from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ugiinbichig.models import Video
from ugiinbichig.serializers import VideoSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser,FormParser
class VideoView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser,FormParser)  # Файл дамжуулахад тохиромжтой парсер

    def get(self, request):
        human = request.query_params.get('human_ID')

        if human:
            # Хүний ID-тай видеог хайх
            videos = Video.objects.filter(human=human)

            # Хэрэв видео байхгүй бол `404` буцаах
            if not videos.exists():  # ✅ QuerySet хоосон эсэхийг шалгах зөв арга
                return Response({"error": "No videos found for this human."}, status=status.HTTP_404_NOT_FOUND)

            # Видео сериализер
            serializer = VideoSerializer(videos, many=True)

            # Хариултад өгөгдлийг буцаах
            return Response({
                "status": "success",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        return Response({"error": "No videos found for this human."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        


    def post(self, request):
    # Human ID-ийг query параметрээс авах
        human = request.query_params.get('human_ID')  
        if not human:
            return Response({"error": "Human ID is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Видео файлыг request.FILES-аас авах
        video_file = request.FILES.get('video')  # video талбарыг video_file болгож тохируулж байгаа нь чухал
        if not video_file:
            return Response({"error": "Video file is required."}, status=status.HTTP_400_BAD_REQUEST)

        # Сериализерт зориулсан өгөгдлийг бэлтгэх
        data = {
            'human': human,
            'video_file': video_file,  # video_file талбар
            'title': request.data.get('title', ''),
            'description': request.data.get('description', '')
        }

        # Сериализерийг шалгаж хадгалах
        serializer = VideoSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)  # Алдааг хэвлэх
            return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        video_id = request.data.get('video_ID')
        video = Video.objects.filter(video_ID=video_id).first()
        if not video:
            return Response({"error": "Video not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = VideoSerializer(video, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        video_id = request.query_params.get('id')
        video = Video.objects.filter(video_ID=video_id).first()
        if not video:
            return Response({"error": "Video not found"}, status=status.HTTP_404_NOT_FOUND)

        video.delete()
        return Response({"message": "Video deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
