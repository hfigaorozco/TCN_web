from django.urls import path
from . import views

urlpatterns = [
    path('horarios/',        views.buscar_corridas,    name='comprarboleto'),
    path('asientos/<int:corrida_id>/', views.seleccionar_asiento, name='seleccionar_asiento'),
    path('confirmacion/',    views.confirmacion_compra, name='confirmacion_compra'),
    path('generar-boletos/', views.generar_boletos,     name='generar_boletos'),
]