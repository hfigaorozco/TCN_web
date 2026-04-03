from django.db import models
from django.core.validators import MinLengthValidator, RegexValidator

class TipoPasajero(models.Model):
    codigo = models.CharField(
        primary_key=True,
        max_length=5,
    )
    
    descripcion = models.CharField(
        max_length=20,
    )
    
    porcentaje_desc = models.PositiveIntegerField()
    
    class Meta:
        db_table = 'tipo_pasajero'
    
    def __str__(self):
        return f"{self.descripcion} ({self.porcentaje_desc}%)"
    

class Pasajero(models.Model):
    numero = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=30)
    apellPat = models.CharField(max_length=20)
    apellMat = models.CharField(max_length=20, null=True, blank=True)
    edad = models.IntegerField()
    correoElect = models.EmailField(max_length=40, null=True, blank=True)
    telefono = models.CharField(max_length=10, null=True, blank=True)

    class Meta:
        db_table = 'pasajero' 

    def __str__(self):
        return f"{self.nombre} {self.apellPat}"