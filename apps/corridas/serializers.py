# apps/corridas/serializers.py
from rest_framework import serializers
from .models import Corrida

class CorridaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Corrida
        fields = ('numero', 'hora_salida', 'fecha_salida', 'hora_llegada', 'fecha_llegada', 'tarifaBase', 'lugaresDisp', 'autobus', 'ruta', 'operador', 'estado')