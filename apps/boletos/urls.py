from django.urls import path
from . import views

urlpatterns = [
    path('horarios/', views.buscar_corridas, name='comprarboleto'),
]