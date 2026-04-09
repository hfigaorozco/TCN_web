from rest_framework.decorators import api_view
from rest_framework.response import Response
from apps.corridas.models import CorridaAsiento
from .serializers import CorridaAsientoSerializer

@api_view(['GET'])
def listar_asientos_corrida_api(request, corrida_id):
    
    asientos = CorridaAsiento.objects.filter(corrida_id=corrida_id)
    serializer = CorridaAsientoSerializer(asientos, many=True)
    return Response(serializer.data)
