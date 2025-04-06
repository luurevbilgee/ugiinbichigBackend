from rest_framework import serializers
from ugiinbichig.models import  Punishment

class PunishmentSerializers(serializers.ModelSerializer):
    class Meta:
        model= Punishment
        fields = ['punishment_id', 'human', 'punishment_time', 'shaltgaan', 'imprisoned']