from django.urls import path
from . import views
from .api_views import registro_api

urlpatterns = [
    path('registro/', views.registro, name='registro'),
    path('api/registro/', registro_api, name = 'registro_api')
]
