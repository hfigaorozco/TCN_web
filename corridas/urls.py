from django.urls import path
from . import views

urlpatterns = [
    path('corridas/', views.pagina_corridas, name='corridas'),
]
