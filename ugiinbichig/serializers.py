from rest_framework import serializers
from .models import User, Human, Who, Image, Death, Divorce, Marry, School, Mergejil, Edu, Health, Lavlah , LavlahEdu, Shape

class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields =[ 'username', 'email','phone_number']

class HumanSerializers(serializers.ModelSerializer):
    class Meta: 
        model = Human
        fields = [ 'urgiin_ovog', 'ovog', 'ys_undes', 'name' , 'RD', 'birth_date', 'birth_counter', 'birth_year', 'gender']

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

class LavlahSerializers(serializers.ModelSerializer):
    class Meta:
        model = Lavlah
        fields = ['lavlah_ID', 'nershil']

class WhoSerializers(serializers.ModelSerializer):
    class Meta:
        model= Who
        fields = ['who_ID', 'human_ID', 'relations_ID', 'lavlah_ID']


class LavlahEduSerializers(serializers.ModelSerializer):
    class Meta:
        model= LavlahEdu
        fields =['lavlahEdu_ID', 'nershil']

class EduSerializers(serializers.ModelSerializer):
    class Meta:
        model= Edu
        fields = ['edu_ID', 'human_ID', 'lavlahEdu_ID']

class SchoolSerializers(serializers.ModelSerializer):
    class Meta:
        model= School
        fields = ['school_ID','human_ID', 'start_time', 'end_time', 'school_name']

class MergejilSerializers(serializers.ModelSerializer):
    class Meta:
        model= Mergejil
        fields= ['mergejil_ID','human_ID','mergejil']

class HealthSerializers(serializers.ModelSerializer):
    class Meta:
        model= Health
        fields=['health_ID', 'human_ID', 'history', 'health_date']

class MarrySerializers(serializers.ModelSerializer):
    class Meta:
        model= Marry
        fields= ['marry_ID', 'human_ID', 'marryd', 'marry_date']

class DivorceSerializers(serializers.ModelSerializer):
    class Meta:
        model= Divorce
        fields = ['divorce_ID', 'human_id', 'divorced', 'divorce_date', 'shaltgaan']

class DeathSerializers(serializers.ModelSerializer):
    class Meta:
        model= Death
        fields = ['death_ID', 'human_ID', 'death_time', 'shaltgaan']

class ImageSerializers(serializers.ModelSerializer):
    image = serializers.ImageField()
    discription = serializers.CharField()
    class Meta:
        model = Image
        fields = [ 'image', 'discription']


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

class SignupSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    phone_number = serializers.CharField()
    password = serializers.CharField(write_only = True)
    
class ShapeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Shape
        fields = ['shape_id', 'x', 'y', 'type', 'color', 'parent_id', 'label', 'human_ID', 'is_verified']