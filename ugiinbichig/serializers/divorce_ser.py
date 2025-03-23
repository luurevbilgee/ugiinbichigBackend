from rest_framework import serializers
from ugiinbichig.models import  Divorce

class DivorceSerializers(serializers.ModelSerializer):
    class Meta:
        model= Divorce
        fields = ['divorce_ID', 'human', 'divorced', 'divorce_date', 'shaltgaan']