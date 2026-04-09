from django.urls import path
from . import views
from .api_views import mis_reservaciones_api  

urlpatterns = [
    path('reservaciones/', views.pagina_reservaciones, name='reservaciones'),
    path('ver-boletos/<int:reserva_id>/', views.ver_boletos_reserva, name='ver_boletos_reserva'),
    path('api/reservaciones/<int:pasajero_id>/', mis_reservaciones_api, name='api_mis_reservaciones'), 
]