from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from .serializers import RegistroSerializer

@api_view(['POST'])
def registro_api(request):
    serializer = RegistroSerializer(data = request.data)
    
    serializer.is_valid(raise_exception=True)
    
    usuario = serializer.save()
    
    return Response({
        'id': usuario.id,
        'nombre': usuario.nombre,
        'email': usuario.email,
        'nombre': usuario.nombre,
    }, status=status.HTTP_201_CREATED)
    