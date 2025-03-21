from rest_framework import serializers
from ugiinbichig.models import  Who

class WhoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Who
        fields = '__all__'