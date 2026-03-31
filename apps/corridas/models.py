# from django.db import models
# from django.core.validators import RegexValidator

# class EdoCorrida(models.Model):
#     codigo = models.CharField(
#         max_length=3,
#         primary_key=True,
#         validators=[
#             RegexValidator(r'^[A-Z]{3}$', 'Solo letras mayúsculas')
#         ]
#     )
#     descripcion = models.CharField(
#         max_length=10,
#         validators=[
#             RegexValidator(r'^[A-Z]{1,10}$', 'Solo letras mayúsculas')
#         ]
#     )
    
#     class Meta:
#         db_table = 'edo_corrida'
    
#     def __str__(self):
#         return self.descripcion

# class Corrida(models.Model):
#     numero = models.AutoField(primary_key=True)
#     hora_salida = models.TimeField(blank=False)
#     fecha_salida = models.DateField(blank=False)
#     hora_llegada = models.TimeField(blank=False)
#     fecha_llegada = models.DateField(blank=False)
#     tarifaBase = models.FloatField(blank=False)
#     #todo: calcular la cantidad de lugares disponibles
#     #lugaresDisp = models.IntegerField
#     autobus = models.ForeignKey(
#         'autobuses.Autobus',
#         db_column = 'autobus',
#         related_name='corridas',
#         on_delete=models.RESTRICT
#     )
#     ruta = models.ForeignKey(
#         'rutas.Ruta',
#         db_column='ruta',
#         related_name='corridas',
#         on_delete=models.RESTRICT
#     )
#     operador = models.ForeignKey(
#         'operadores.Operador',
#         db_column='operador',
#         related_name='corridas',
#         on_delete=models.RESTRICT
#     )
#     estado = models.ForeignKey(
#         'EdoCorrida', 
#         on_delete=models.RESTRICT, 
#         db_column='estado', 
#         related_name='corridas'
#     )
    
#     class Meta:
#         db_table = 'corrida'
    
#     def __str__(self):
#         return f'Corrida {self.numero} - {self.fecha_salida} - {self.ruta}'
# # Create your models here.




# # CREATE TABLE edo_corrida(
# #     codigo VARCHAR(3) PRIMARY KEY,
# #     descripcion VARCHAR(10) NOT NULL UNIQUE
# # );

# # CREATE TABLE corrida(
# #     numero INT PRIMARY KEY AUTO_INCREMENT, 
# #     hora_salida TIME NOT NULL, 
# #     fecha_salida DATE NOT NULL,
# #     hora_llegada TIME NOT NULL,
# #     fecha_llegada DATE NOT NULL, 
# #     tarifaBase FLOAT NOT NULL, 
# #     lugaresDisp INT NOT NULL,
# #     autobus INT NOT NULL, 
# #     ruta VARCHAR(9) NOT NULL,
# #     operador INT, 
# #     estado VARCHAR(3) NOT NULL 
# # );

# # ALTER TABLE corrida
# # ADD CONSTRAINT fk_corrida_autobus
# # FOREIGN KEY (autobus) REFERENCES autobus(numero)
# # ON UPDATE CASCADE ON DELETE RESTRICT;

# # ALTER TABLE corrida
# # ADD CONSTRAINT fk_corrida_ruta
# # FOREIGN KEY (ruta) REFERENCES ruta(codigo)
# # ON UPDATE CASCADE ON DELETE RESTRICT;

# # ALTER TABLE corrida
# # ADD CONSTRAINT fk_corrida_operador
# # FOREIGN KEY (operador) REFERENCES operador(numero)
# # ON UPDATE CASCADE ON DELETE RESTRICT;

# # ALTER TABLE corrida
# # ADD CONSTRAINT fk_corrida_estado
# # FOREIGN KEY (estado) REFERENCES edo_corrida(codigo)
# # ON UPDATE CASCADE ON DELETE RESTRICT;