from rest_framework import serializers
from ugiinbichig.models import  Mergejil
class MergejilSerializers(serializers.ModelSerializer):
    class Meta:
        model= Mergejil
        fields= ['mergejil_ID','human_ID','mergejil']
