from django.db import models
from django.core.validators import MinLengthValidator, RegexValidator

class EdoCorrida(models.Model):
    
    codigo = models.CharField(
        max_length=3,
        primary_key=True
    )
    
    descripcion = models.CharField(
        max_length=10
    )
    
    class Meta:
        db_table = 'edo_corrida'
    
    def __str__(self):
        return f"{self.codigo} - {self.descripcion}"