from ..login.models import Usuario
from rest_framework import viewsets, premissions

class UsuarioViewSet(viewsets.ModelViewSet):
    Usuario.objects.all()