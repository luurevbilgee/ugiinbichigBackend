from rest_framework import serializers
from ugiinbichig.models.profile_model import ProfilePicture

class ProfilePictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfilePicture
        fields = ['human', 'image', 'description', 'created_at']
