from rest_framework import serializers
from ugiinbichig.models import  Death

class DeathSerializers(serializers.ModelSerializer):
    class Meta:
        model= Death
        fields = ['death_ID', 'human_ID', 'death_time', 'shaltgaan']