from django.db import models


class Reservacion(models.Model):
    numero        = models.AutoField(primary_key=True)
    fecha         = models.DateField()
    fechaLimPago  = models.DateField()
    cantPasajeros = models.IntegerField()
    subtotal      = models.FloatField()
    IVA           = models.FloatField()
    total         = models.FloatField()
    pasajero      = models.ForeignKey(
        'pasajeros.Pasajero',
        on_delete=models.RESTRICT,
        db_column='pasajero',
        related_name='reservaciones',
    )
    corrida       = models.ForeignKey(
        'corridas.Corrida',
        on_delete=models.RESTRICT,
        db_column='corrida',
        related_name='reservaciones',
    )

    class Meta:
        db_table = 'reservacion'

    def __str__(self):
        return f'Reservación {self.numero} - {self.pasajero}'


class AsientoReservacion(models.Model):
    asiento     = models.ForeignKey(
        'autobuses.Asiento',
        on_delete=models.RESTRICT,
        db_column='asiento',
        related_name='asiento_reservaciones',
    )
    reservacion = models.ForeignKey(
        'Reservacion',
        on_delete=models.RESTRICT,
        db_column='reservacion',
        related_name='asiento_reservaciones',
    )

    class Meta:
        db_table        = 'asiento_reservacion'
        unique_together = ('asiento', 'reservacion')

    def __str__(self):
        return f'Asiento {self.asiento_id} - Reservación {self.reservacion_id}'