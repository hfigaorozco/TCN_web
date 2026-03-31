from django.urls import path
from . import views

urlpatterns = [
    path('reservaciones/', views.pagina_reservaciones, name='reservaciones')
]
