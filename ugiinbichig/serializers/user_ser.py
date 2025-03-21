from rest_framework import serializers
from ugiinbichig.models import User
class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields =[ 'username', 'email','phone_number']