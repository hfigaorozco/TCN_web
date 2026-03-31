from django.urls import path
from . import views

urlpatterns = [
    path('operadores/', views.pagina_operadores, name='operadores'),
]
