from rest_framework import serializers
from .models import registration


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = registration
        fields ='__all__'
