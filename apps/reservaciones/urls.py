from django.urls import path
from . import views

urlpatterns = [
    path('reservaciones/', views.pagina_reservaciones, name='reservaciones'),
    path('ver-boletos/<int:reserva_id>/', views.ver_boletos_reserva, name='ver_boletos_reserva'),
]
