from rest_framework import serializers
from ugiinbichig.models import  Marry



class MarrySerializers(serializers.ModelSerializer):
    class Meta:
        model= Marry
        fields= ['marry_ID', 'human', 'marryd', 'marry_date']