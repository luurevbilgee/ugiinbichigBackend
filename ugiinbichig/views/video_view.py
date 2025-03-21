from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ugiinbichig.models import Video
from ugiinbichig.serializers import VideoSerializer
from rest_framework.permissions import IsAuthenticated

class VideoView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        video_id = request.query_params.get('id')
        if video_id:
            video = Video.objects.filter(video_ID=video_id).first()
            if not video:
                return Response({"error": "Video not found"}, status=status.HTTP_404_NOT_FOUND)
            serializer = VideoSerializer(video)
        else:
            videos = Video.objects.all()
            serializer = VideoSerializer(videos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = VideoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
