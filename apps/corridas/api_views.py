from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Corrida, CorridaAsiento
from .serializers import CorridaSerializer, CorridaAsientoSerializer


@api_view(['GET'])
def listar_corridas_api(request):
    corridas = Corrida.objects.filter(
        estado__codigo='ACT'
    ).select_related('estado', 'autobus__tipoAutobus')
    serializer = CorridaSerializer(corridas, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def buscar_corridas_api(request):
    origen = request.GET.get('origen')
    destino = request.GET.get('destino')
    fecha = request.GET.get('fecha')
    pasajeros = int(request.GET.get('pasajeros', 1))

    if not origen or not destino or not fecha:
        return Response(
            {'error': 'Faltan parámetros: origen, destino, fecha'},
            status=status.HTTP_400_BAD_REQUEST
        )

    corridas = Corrida.objects.filter(
        estado__codigo='ACT',
        fecha_salida=fecha,
        ruta__ciudadOrigen__nombre=origen,
        ruta__ciudadDestino__nombre=destino,
        lugaresDisp__gte=pasajeros
    ).select_related(
        'estado',
        'autobus',
        'autobus__tipoAutobus',   # necesario para tipoAutobus en serializer
        'ruta',
        'ruta__ciudadOrigen',
        'ruta__ciudadDestino',
    )

    serializer = CorridaSerializer(corridas, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def consultar_asientos_api(request, corrida_id):
    try:
        corrida = Corrida.objects.get(pk=corrida_id)
    except Corrida.DoesNotExist:
        return Response(
            {'error': f'No existe una corrida con id {corrida_id}'},
            status=status.HTTP_404_NOT_FOUND
        )

    asientos = CorridaAsiento.objects.filter(
        corrida=corrida
    ).select_related('asiento')

    serializer = CorridaAsientoSerializer(asientos, many=True)
    return Response(serializer.data)