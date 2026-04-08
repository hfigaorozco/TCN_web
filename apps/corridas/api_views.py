from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Corrida
from .serializers import CorridaSerializer

@api_view(['GET'])
def listar_corridas_api(request):
    corridas = Corrida.objects.filter(estado='ACT')
    
    serializer = CorridaSerializer(corridas, many=True)
    
    return Response(serializer.data)