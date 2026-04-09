from rest_framework import serializers
from .models import Reservacion, AsientoReservacion
from apps.boletos.models import Boleto
from apps.autobuses.models import Asiento
from apps.rutas.models import Ciudad, Ruta
from apps.corridas.models import Corrida
from apps.pasajeros.models import TipoPasajero, Pasajero


class TipoPasajeroSerializer(serializers.ModelSerializer):
    class Meta:
        model  = TipoPasajero
        fields = ['codigo', 'descripcion', 'porcentaje_desc']


class AsientoSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Asiento
        fields = ['clave', 'numero', 'ubicacion']


class PasajeroSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Pasajero
        fields = ['numero', 'nombre', 'apellPat', 'apellMat']


class BoletoSerializer(serializers.ModelSerializer):
    asiento      = AsientoSerializer()
    tipoPasajero = TipoPasajeroSerializer()
    pasajero     = PasajeroSerializer()   # nuevo

    class Meta:
        model  = Boleto
        fields = ['numero', 'precio', 'asiento', 'tipoPasajero', 'pasajero']


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
    ruta    = RutaSerializer()
    estado  = serializers.CharField(source='estado.codigo')
    autobus = serializers.IntegerField(source='autobus.numero')  # nuevo

    class Meta:
        model  = Corrida
        fields = ['numero', 'hora_salida', 'fecha_salida', 'hora_llegada',
                  'fecha_llegada', 'tarifaBase', 'ruta', 'estado', 'autobus']


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
        asientos_clave = AsientoReservacion.objects.filter(
            reservacion=reservacion
        ).values_list('asiento', flat=True)

        qs = Boleto.objects.filter(
            corrida=reservacion.corrida,
            asiento__in=asientos_clave,
        ).select_related('asiento', 'tipoPasajero', 'pasajero')  

        return BoletoSerializer(qs, many=True).data