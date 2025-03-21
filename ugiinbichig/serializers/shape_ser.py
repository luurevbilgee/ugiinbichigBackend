from rest_framework import serializers
from ugiinbichig.models import  Shape




    
class ShapeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Shape
        fields = ['shape_id', 'x', 'y', 'type', 'color', 'parent_id', 'label', 'human_ID']