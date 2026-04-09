from django.urls import path
from . import views
from .api_views import listar_corridas_api, consultar_asientos_api, buscar_corridas_api

urlpatterns = [
    path('corridas/', views.pagina_corridas, name='corridas'),
    path('api/corridas/', listar_corridas_api, name='api_corridas'),
    path('api/corridas/buscar/', buscar_corridas_api, name='api_buscar_corridas'),       
    path('api/corridas/<int:corrida_id>/asientos/', consultar_asientos_api, name='api_asientos_corrida'),
]