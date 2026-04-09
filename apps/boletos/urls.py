from django.urls import path
from . import views
from .api_views import generar_boletos_api

urlpatterns = [
    path('horarios/', views.buscar_corridas, name='comprarboleto'),
    path('asientos/<int:corrida_id>/', views.seleccionar_asiento, name='seleccionar_asiento'),
    path('confirmacion/', views.confirmacion_compra, name='confirmacion_compra'),
    path('generar-boletos/', views.generar_boletos, name='generar_boletos'),
    path('ver-boletos/<int:reserva_id>/', views.ver_boletos, name='ver_boletos'),
    path('api/generar-boletos/', generar_boletos_api, name='api_generar_boletos'),
]