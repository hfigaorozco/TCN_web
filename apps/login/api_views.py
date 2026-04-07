from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from ..registro.serializers import RegistroSerializer
from .serializers import LoginSerializer

@api_view(['POST'])
def login_api(request):
    serializer = LoginSerializer(data = request.data)
    
    serializer.is_valid(raise_exception=True)
    
    user = serializer.validated_data['user']
    
    token, created = Token.objects.get_or_create(user=user)
    
    return Response({
        'token': token.key,
        'user_id': user.id,
        'email': user.email,
        'nombre': user.nombre
    })

