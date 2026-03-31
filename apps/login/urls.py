from django.urls import path
from . import views

urlpatterns = [
    path('inicio-de-sesion/', views.inicio_sesion, name='login'),
]