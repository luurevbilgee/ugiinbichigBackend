from rest_framework import serializers
from ugiinbichig.models import School

class SchoolSerializers(serializers.ModelSerializer):
    class Meta:
        model= School
        fields = ['school_ID','human_ID', 'start_time', 'end_time', 'school_name','zereg']