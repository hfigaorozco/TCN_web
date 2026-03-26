from django.shortcuts import render

# Create your views here.

def pagina_rutas(request):
    return render(request, 'rutas.html')