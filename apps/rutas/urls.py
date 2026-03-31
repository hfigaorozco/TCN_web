from django.urls import path
from . import views

urlpatterns = [
    path('rutas/', views.pagina_rutas, name='rutas'),
]
