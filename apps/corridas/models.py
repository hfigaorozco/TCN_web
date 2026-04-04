from django.db import models
from django.core.validators import RegexValidator


class EdoCorrida(models.Model):
    codigo = models.CharField(
        max_length=3,
        primary_key=True,
        validators=[RegexValidator(r'^[A-Z]{3}$', 'Solo letras mayúsculas')]
    )
    descripcion = models.CharField(
        max_length=10,
        validators=[RegexValidator(r'^[A-Z]{1,10}$', 'Solo letras mayúsculas')]
    )

    class Meta:
        db_table = 'edo_corrida'

    def __str__(self):
        return self.descripcion


class Corrida(models.Model):
    numero        = models.AutoField(primary_key=True)
    hora_salida   = models.TimeField(blank=False)
    fecha_salida  = models.DateField(blank=False)
    hora_llegada  = models.TimeField(blank=False)
    fecha_llegada = models.DateField(blank=False)
    tarifaBase    = models.FloatField(blank=False)
    lugaresDisp   = models.IntegerField()
    autobus       = models.ForeignKey(
        'autobuses.Autobus',
        db_column='autobus',
        related_name='corridas',
        on_delete=models.RESTRICT
    )
    ruta          = models.ForeignKey(
        'rutas.Ruta',
        db_column='ruta',
        related_name='corridas',
        on_delete=models.RESTRICT
    )
    operador      = models.ForeignKey(
        'operadores.Operador',
        db_column='operador',
        related_name='corridas',
        on_delete=models.RESTRICT
    )
    estado        = models.ForeignKey(
        'EdoCorrida',
        on_delete=models.RESTRICT,
        db_column='estado',
        related_name='corridas'
    )

    class Meta:
        db_table = 'corrida'

    def __str__(self):
        return f'Corrida {self.numero} - {self.fecha_salida} - {self.ruta}'


class CorridaAsiento(models.Model):
    DISPONIBLE = 'DISPONIBLE'
    OCUPADO    = 'OCUPADO'
    RESERVADO  = 'RESERVADO'

    ESTADO_CHOICES = [
        (DISPONIBLE, 'Disponible'),
        (OCUPADO,    'Ocupado'),
        (RESERVADO,  'Reservado'),
    ]

    corrida = models.ForeignKey(
        'Corrida',
        on_delete=models.CASCADE,
        db_column='corrida',
        related_name='corrida_asientos'
    )
    asiento = models.ForeignKey(
        'autobuses.Asiento',
        on_delete=models.RESTRICT,
        db_column='asiento',
        related_name='corrida_asientos'
    )
    estado  = models.CharField(
        max_length=13,
        choices=ESTADO_CHOICES,
        default=DISPONIBLE
    )

    class Meta:
        db_table        = 'corrida_asiento'
        unique_together = ('corrida', 'asiento')

    def __str__(self):
        return f'Corrida {self.corrida_id} - Asiento {self.asiento_id} - {self.estado}'