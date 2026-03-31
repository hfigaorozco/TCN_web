from django.db import models
from django.core.validators import RegexValidator
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class Operador(models.Model):
    numero = models.AutoField(primary_key=True)
    nombre = models.CharField(
        max_length=15, 
        validators=[
            RegexValidator(r'^[A-Za-záéíóúñÁÉÍÓÚÑ]+$', 'Solo se permiten letras')
        ]
    )
    apellPat = models.CharField(
        max_length=15, 
        validators=[
            RegexValidator(r'^[A-Za-záéíóúñÁÉÍÓÚÑ]+$', 'Solo se permiten letras')
        ]
    )
    apellMat = models.CharField(
        max_length=15, 
        blank=True,
        null=True,
        validators=[
            RegexValidator(r'^[A-Za-záéíóúñÁÉÍÓÚÑ]+$', 'Solo se permiten letras')
        ]
    )
    fechaNac = models.DateField()
    telefono = models.CharField(
        max_length=10,
        unique=True,
        validators=[
            RegexValidator(r'^[0-9]{10}$', 'El teléfono debe tener exactamente 10 dígitos')
        ]
    )
    fechaContrato=models.DateField()
    
    
    class Meta:
        db_table = 'operador'
    
    def __str__(self):
        return f"Operador {self.numero} - {self.nombre} {self.apellPat}"