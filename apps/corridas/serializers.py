from rest_framework import serializers
from .models import Corrida, CorridaAsiento

class CorridaSerializer(serializers.ModelSerializer):
    estado = serializers.CharField(source='estado.codigo')  # devuelve 'ACT' en vez del objeto FK
    class Meta:
        model = Corrida
        fields = (
            'numero', 'hora_salida', 'fecha_salida',
            'hora_llegada', 'fecha_llegada', 'tarifaBase',
            'lugaresDisp', 'autobus', 'ruta', 'operador', 'estado'
        )

class CorridaAsientoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CorridaAsiento
        fields = ('corrida', 'asiento', 'estado')