from django.shortcuts import render

# Create your views here.

def pagina_reservaciones(request):
    return render(request, 'reservaciones.html')