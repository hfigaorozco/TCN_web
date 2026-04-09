from rest_framework import serializers
from apps.corridas.models import CorridaAsiento
from apps.autobuses.models import Asiento

class AsientoBaseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Asiento
        fields = ['clave', 'numero', 'ubicacion']

class CorridaAsientoSerializer(serializers.ModelSerializer):
    
    asiento_info = AsientoBaseSerializer(source='asiento', read_only=True)
    
    class Meta:
        model = CorridaAsiento
        fields = ['id', 'corrida', 'asiento', 'asiento_info', 'estado']
