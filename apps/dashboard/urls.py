# dashboard/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.index, name='index'),
    path('dashboard/corrida/<int:corrida_id>/', views.get_corrida_details, name='get_corrida_details'),
    path('dashboard/cambiar-contrasena/', views.cambiar_contrasena, name='cambiar_contrasena'),
]