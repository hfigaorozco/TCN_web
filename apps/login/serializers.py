from .models import Usuario
from rest_framework import serializers
from django.contrib.auth import authenticate


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    
    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        
        usuario = authenticate(email = email, password = password)
        
        if not usuario:
            raise serializers.ValidationError('La contraseña o el correo electrónico es incorrecto')
        else:
            data['user'] = usuario
        
        return data

class CambiarContraSerializer(serializers.Serializer):
    actual_password = serializers.CharField();
    nuevo_password = serializers.CharField();
    
    def validate(self, data):
        usuario = self.context.get('usuario')
        
        actual_password = data.get('actual_password')
        nuevo_password = data.get('nuevo_password')
        
        if not usuario.check_password(actual_password):
            raise serializers.ValidationError('Contraseña incorrecta')
        
        return data