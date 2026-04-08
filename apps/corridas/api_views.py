from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Corrida, CorridaAsiento
from .serializers import CorridaSerializer, CorridaAsientoSerializer

@api_view(['GET'])
def listar_corridas_api(request):
    corridas = Corrida.objects.filter(estado__codigo='ACT')  
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