from django.db import models
from django.core.validators import RegexValidator


class Ciudad(models.Model):
    codigo = models.CharField(
        max_length=3,
        primary_key=True
    )
    nombre = models.CharField(
        max_length=20,
        unique=True
    )

    class Meta:
        db_table = 'ciudad'

    def __str__(self):
        return self.nombre


class Ruta(models.Model):
    codigo = models.CharField(
        max_length=7,
        primary_key=True,
        validators=[
            RegexValidator(
                r'^[A-Z0-9]{1,5}$',
                'Solo letras mayúsculas y números'
            )
        ]
    )

    ciudadOrigen = models.ForeignKey(
        Ciudad,
        on_delete=models.PROTECT,
        related_name='rutas_origen',
        db_column='ciudadOrigen'
    )

    ciudadDestino = models.ForeignKey(
        Ciudad,
        on_delete=models.PROTECT,
        related_name='rutas_destino',
        db_column='ciudadDestino'
    )

    distancia = models.FloatField()

    class Meta:
        db_table = 'ruta'

    def __str__(self):
        return f"{self.ciudadOrigen} → {self.ciudadDestino}"