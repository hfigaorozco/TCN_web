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