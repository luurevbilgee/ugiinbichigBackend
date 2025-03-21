from rest_framework import serializers
from ugiinbichig.models import  Image


class ImageSerializers(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = [ 'image', 'discription']
