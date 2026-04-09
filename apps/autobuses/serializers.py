from rest_framework import serializers
from .models import Autobus, TipoAutobus


class TipoAutobusSerializer(serializers.ModelSerializer):
    class Meta:
        model  = TipoAutobus
        fields = ['codigo', 'descripcion']


class AutobusSerializer(serializers.ModelSerializer):
    tipoAutobus = TipoAutobusSerializer()  

    class Meta:
        model  = Autobus
        fields = ['numero', 'matricula', 'cantAsientos', 'tipoAutobus']