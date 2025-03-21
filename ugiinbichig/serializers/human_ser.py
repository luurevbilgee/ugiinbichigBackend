from rest_framework import serializers
from ugiinbichig.models import  Human
class HumanSerializers(serializers.ModelSerializer):
    class Meta: 
        model = Human
        fields = ['urgiin_ovog', 'ovog', 'ys_undes', 'name' , 'RD', 'birth_date', 'birth_counter', 'birth_year', 'gender']

class HumanSaveSerializers(serializers.ModelSerializer):
    urgiin_ovog = serializers.CharField()
    ovog = serializers.CharField()
    ys_undes = serializers.CharField()
    name = serializers.CharField()
    RD = serializers.CharField()
    birth_date = serializers.DateField()
    birth_counter = serializers.CharField()
    birth_year = serializers.CharField()
    gender = serializers.CharField()
    class Meta:
        model = Human  # Энэ нь Human загварын өгөгдлийг сериализ хийхийг зааж байна
        fields = [
            'urgiin_ovog', 'ovog', 'ys_undes', 'name', 'RD', 
            'birth_date', 'birth_counter', 'birth_year', 'gender'
        ]