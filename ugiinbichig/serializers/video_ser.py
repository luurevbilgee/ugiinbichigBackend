from rest_framework import serializers
from ugiinbichig.models import  Video


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ['video_ID', 'human', 'title', 'description', 'video_file', 'uploaded_at']