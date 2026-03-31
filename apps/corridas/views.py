from django.shortcuts import render

# Create your views here.

def pagina_corridas(request):
    return render(request, 'corridas.html')

