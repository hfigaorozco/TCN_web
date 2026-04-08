from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Ciudad
from .serializers import CiudadSerializer

@api_view(['GET'])
def listar_ciudades_api(request):
    
    ciudades = Ciudad.objects.all()
    serializer = CiudadSerializer(ciudades, many=True)
    return Response(serializer.data)
