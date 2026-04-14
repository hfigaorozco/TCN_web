from django.urls import path
from . import views
from .api_views import login_api, cambiar_contra_api

urlpatterns = [
    path('inicio-de-sesion/', views.inicio_sesion, name='login'),
    path('api/login/', login_api, name = 'api_login'),
    path('api/contraseña/', cambiar_contra_api, name='api_cambiar')
]