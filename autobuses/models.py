from django.db import models
from django.core.validators import MinLengthValidator, RegexValidator


class Marca(models.Model):
    clave = models.CharField(
        max_length=5,
        primary_key=True,
        validators=[
            RegexValidator(r'^[A-Z0-9]{1,5}$', 'Solo letras mayúsculas y números')
        ]
    )
    nombre = models.CharField(max_length=15)

    class Meta:
        db_table = 'marca'

    def __str__(self):
        return self.nombre


class Modelo(models.Model):
    clave = models.CharField(
        max_length=5,
        primary_key=True,
        validators=[
            RegexValidator(r'^[A-Z0-9]{1,5}$', 'Solo letras mayúsculas y números')
        ]
    )
    nombre = models.CharField(max_length=15)
    marca = models.ForeignKey('Marca', on_delete=models.PROTECT)

    class Meta:
        db_table = 'modelo'

    def __str__(self):
        return self.nombre


class TipoAutobus(models.Model):
    codigo = models.CharField(
        max_length=4,
        primary_key=True,
        validators=[
            RegexValidator(r'^[A-Z0-9]{1,4}$', 'Solo letras mayúsculas y números')
        ]
    )
    descripcion = models.CharField(max_length=10)

    class Meta:
        db_table = 'tipo_autobus'

    def __str__(self):
        return self.descripcion


class EdoAutobus(models.Model):
    codigo = models.CharField(
        max_length=4,
        primary_key=True,
        validators=[
            RegexValidator(r'^[A-Z0-9]{1,4}$', 'Solo letras mayúsculas y números')
        ]
    )
    descripcion = models.CharField(max_length=10)

    class Meta:
        db_table = 'edo_autobus'

    def __str__(self):
        return self.descripcion


class Autobus(models.Model):
    numero = models.IntegerField(primary_key=True)
    matricula = models.CharField(
        max_length=6,
        unique=True,
        validators=[
            RegexValidator(r'^[A-Z0-9]{6}$', 'Debe tener exactamente 6 caracteres alfanuméricos')
        ]
    )
    claveWIFI = models.CharField(max_length=20, null=True, blank=True)
    cantAsientos = models.PositiveIntegerField()
    tipoAutobus = models.ForeignKey('TipoAutobus', on_delete=models.PROTECT)
    estado = models.ForeignKey('EdoAutobus', on_delete=models.PROTECT)
    marca = models.ForeignKey('Marca', on_delete=models.PROTECT)
    modelo = models.ForeignKey('Modelo', on_delete=models.PROTECT)

    class Meta:
        db_table = 'autobus'

    def __str__(self):
        return f"Autobús {self.numero} - {self.matricula}"