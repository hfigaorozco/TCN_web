from rest_framework import serializers
from .models import Corrida, CorridaAsiento


class CorridaSerializer(serializers.ModelSerializer):
    estado = serializers.CharField(source='estado.codigo')
    ciudadOrigen = serializers.CharField(source='ruta.ciudadOrigen.nombre')
    ciudadDestino = serializers.CharField(source='ruta.ciudadDestino.nombre')
    tipoAutobus = serializers.CharField(source='autobus.tipoAutobus.codigo')

    class Meta:
        model = Corrida
        fields = (
            'numero', 'hora_salida', 'fecha_salida',
            'hora_llegada', 'fecha_llegada', 'tarifaBase',
            'lugaresDisp', 'autobus', 'ruta', 'operador',
            'estado', 'ciudadOrigen', 'ciudadDestino', 'tipoAutobus',
        )


class CorridaAsientoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CorridaAsiento
        fields = ('corrida', 'asiento', 'estado')