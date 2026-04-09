from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Autobus
from .serializers import AutobusSerializer


@api_view(['GET'])
def obtener_autobus_api(request, autobus_id):
    try:
        autobus = Autobus.objects.select_related('tipoAutobus').get(pk=autobus_id)
    except Autobus.DoesNotExist:
        return Response(
            {'error': f'No existe un autobús con id {autobus_id}'},
            status=status.HTTP_404_NOT_FOUND
        )

    serializer = AutobusSerializer(autobus)
    return Response(serializer.data)