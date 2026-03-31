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