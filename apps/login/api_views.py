from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .serializers import LoginSerializer, CambiarContraSerializer
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

@api_view(['POST'])
def login_api(request):
    serializer = LoginSerializer(data = request.data)
    
    serializer.is_valid(raise_exception=True)
    
    user = serializer.validated_data['user']
    
    token, created = Token.objects.get_or_create(user=user)
    
    return Response({
        'token': token.key,
        'id': user.id,
        'email': user.email,
        'nombre': user.nombre
    })

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def cambiar_contra_api(request):
    serializer = CambiarContraSerializer(data = request.data, context={'usuario':request.user});
    serializer.is_valid(raise_exception=True)
    user = request.user
    nuevo_password = serializer.validated_data['nuevo_password']
    user.set_password(nuevo_password)
    user.save()
    
    return Response(status=status.HTTP_204_NO_CONTENT)