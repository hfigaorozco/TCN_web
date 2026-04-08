from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Reservacion
from .serializers import ReservacionSerializer


@api_view(['GET'])
def mis_reservaciones_api(request, pasajero_id):
    
    # Traer todas las reservaciones del pasajero
    reservaciones = Reservacion.objects.filter(
        pasajero__numero=pasajero_id
    ).select_related(
        'corrida',
        'corrida__ruta',
        'corrida__ruta__ciudadOrigen',
        'corrida__ruta__ciudadDestino',
        'corrida__estado',
    )

    if not reservaciones.exists():
        return Response(
            {'mensaje': 'No se encontraron reservaciones para este pasajero'},
            status=status.HTTP_404_NOT_FOUND
        )

    serializer = ReservacionSerializer(reservaciones, many=True)
    return Response(serializer.data)