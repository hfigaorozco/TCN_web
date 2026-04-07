from ..login.models import Usuario
from rest_framework import serializers

class RegistroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ('id', 'nombre', 'email', 'password')
        extra_kwargs = {
            'password': {'write_only': True}
        }
        
    def create(self, validated_data):
        return Usuario.objects.create_user(**validated_data)
    
    
    #Validar que el email exista
    def validate_email(self, value):
        if Usuario.objects.filter(email = value).exists():
            raise serializers.ValidationError("Ya existe una cuenta con este correo electrónico.")
        return value