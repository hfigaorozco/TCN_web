from django.urls import path
from . import views

urlpatterns = [
    path('autobuses/', views.pagina_autobuses, name='autobuses')
]