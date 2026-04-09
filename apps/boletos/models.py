from django.db import models

class Boleto(models.Model):
    numero      = models.AutoField(primary_key=True)
    precio      = models.FloatField()
    asiento     = models.ForeignKey(
        'autobuses.Asiento',
        on_delete=models.RESTRICT,
        db_column='asiento',
        related_name='boletos',
    )
    pasajero    = models.ForeignKey(
        'pasajeros.Pasajero',
        on_delete=models.RESTRICT,
        db_column='pasajero',
        related_name='boletos',
    )
    tipoPasajero = models.ForeignKey(
        'pasajeros.TipoPasajero',
        on_delete=models.RESTRICT,
        db_column='tipoPasajero',
        related_name='boletos',
    )
    corrida     = models.ForeignKey(
        'corridas.Corrida',
        on_delete=models.RESTRICT,
        db_column='corrida',
        related_name='boletos',
    )

    class Meta:
        db_table = 'boleto'

    def __str__(self):
        return f'Boleto {self.numero} - {self.pasajero} - Asiento {self.asiento_id}'