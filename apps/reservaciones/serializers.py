from rest_framework import serializers
from .models import Reservacion
from boletos.models import Boleto
from autobuses.models import Asiento
from rutas.models import Ciudad, Ruta
from corridas.models import Corrida
from pasajeros.models import TipoPasajero


class TipoPasajeroSerializer(serializers.ModelSerializer):
    class Meta:
        model  = TipoPasajero
        fields = ['codigo', 'descripcion', 'porcentaje_desc']  


class AsientoSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Asiento
        fields = ['clave', 'numero', 'ubicacion']


class BoletoSerializer(serializers.ModelSerializer):
    asiento      = AsientoSerializer()
    tipoPasajero = TipoPasajeroSerializer()

    class Meta:
        model  = Boleto
        fields = ['numero', 'precio', 'asiento', 'tipoPasajero']


class CiudadSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Ciudad
        fields = ['codigo', 'nombre']


class RutaSerializer(serializers.ModelSerializer):
    ciudadOrigen  = CiudadSerializer()
    ciudadDestino = CiudadSerializer()

    class Meta:
        model  = Ruta
        fields = ['codigo', 'distancia', 'ciudadOrigen', 'ciudadDestino']


class CorridaResumenSerializer(serializers.ModelSerializer):
    ruta   = RutaSerializer()
    estado = serializers.CharField(source='estado.codigo')

    class Meta:
        model  = Corrida
        fields = ['numero', 'hora_salida', 'fecha_salida', 'hora_llegada', 'tarifaBase', 'ruta', 'estado']


class ReservacionSerializer(serializers.ModelSerializer):
    corrida = CorridaResumenSerializer()
    boletos = serializers.SerializerMethodField()

    class Meta:
        model  = Reservacion
        fields = [
            'numero', 'fecha', 'fechaLimPago',
            'cantPasajeros', 'subtotal', 'IVA', 'total',
            'corrida', 'boletos',
        ]

    def get_boletos(self, reservacion):
        qs = Boleto.objects.filter(
            corrida=reservacion.corrida,
            pasajero=reservacion.pasajero
        ).select_related('asiento', 'tipoPasajero')
        return BoletoSerializer(qs, many=True).data