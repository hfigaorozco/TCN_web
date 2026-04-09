from django.urls import path
from . import views
from .api_views import obtener_autobus_api

urlpatterns = [
    path('autobuses/', views.pagina_autobuses, name='autobuses'),
    path('api/autobuses/<int:autobus_id>/', obtener_autobus_api, name='api_obtener_autobus'),
]