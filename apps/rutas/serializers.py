from rest_framework import serializers
from .models import Ciudad

class CiudadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ciudad
        fields = ['codigo', 'nombre']
