from django.urls import path
from .views import rutas_view, agregar_ciudad, editar_ciudad, agregar_ruta, editar_ruta

urlpatterns = [
    path('rutas/', rutas_view, name='rutas'),
    path('agregar-ciudad/', agregar_ciudad, name='agregar_ciudad'),
    path('editar-ciudad/', editar_ciudad, name='editar_ciudad'),
    path('agregar-ruta/', agregar_ruta, name='agregar_ruta'),
    path('editar-ruta/', editar_ruta, name='editar_ruta'),
]