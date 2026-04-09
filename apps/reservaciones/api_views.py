from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Reservacion
from .serializers import ReservacionSerializer


@api_view(['GET'])
def mis_reservaciones_api(request, pasajero_id):
    reservaciones = Reservacion.objects.filter(
        usuario__id=pasajero_id   
    ).select_related(
        'corrida', 'corrida__ruta',
        'corrida__ruta__ciudadOrigen',
        'corrida__ruta__ciudadDestino',
        'corrida__estado',
    )

    if not reservaciones.exists():
        return Response(
            {'mensaje': 'No se encontraron reservaciones'},
            status=status.HTTP_404_NOT_FOUND
        )

    serializer = ReservacionSerializer(reservaciones, many=True)
    return Response(serializer.data)