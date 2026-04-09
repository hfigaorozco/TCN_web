from django.urls import path
from .views import rutas_view, agregar_ciudad, editar_ciudad, agregar_ruta, editar_ruta
from .api_views import listar_ciudades_api

urlpatterns = [
    path('rutas/', rutas_view, name='rutas'),
    path('agregar-ciudad/', agregar_ciudad, name='agregar_ciudad'),
    path('editar-ciudad/', editar_ciudad, name='editar_ciudad'),
    path('agregar-ruta/', agregar_ruta, name='agregar_ruta'),
    path('editar-ruta/', editar_ruta, name='editar_ruta'),

    path('api/ciudades/', listar_ciudades_api, name='listar_ciudades_api'),
]