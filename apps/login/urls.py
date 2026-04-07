from django.urls import path
from . import views
from .api_views import login_api

urlpatterns = [
    path('inicio-de-sesion/', views.inicio_sesion, name='login'),
    path('api/login/', login_api, name = 'api_login'),
]