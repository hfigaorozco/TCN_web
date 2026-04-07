from django.urls import path
from . import views
from .api_views import listar_corridas_api

urlpatterns = [
    path('corridas/', views.pagina_corridas, name='corridas'),
    path('api/corridas/', listar_corridas_api, name='api_corridas')
]
