from rest_framework import serializers
from ugiinbichig.models import Health
class HealthSerializers(serializers.ModelSerializer):
    class Meta:
        model= Health
        fields=['health_ID', 'human_ID', 'history', 'health_date']