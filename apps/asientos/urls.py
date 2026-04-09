from django.urls import path
from .api_views import listar_asientos_corrida_api

urlpatterns = [
    
    path('api/corrida/<int:corrida_id>/', listar_asientos_corrida_api, name='listar_asientos_corrida_api'),
]
