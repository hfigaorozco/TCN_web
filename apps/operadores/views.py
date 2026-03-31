from django.shortcuts import render

# Create your views here.

def pagina_operadores(request):
    return render(request, 'operadores.html')