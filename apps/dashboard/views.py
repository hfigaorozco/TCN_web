from django.shortcuts import render
from apps.rutas.models import Ciudad

def index(request):
    context = {
        'ciudades': Ciudad.objects.all(),
    }
    
    return render(request, 'index.html', context)