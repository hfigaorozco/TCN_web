from django.shortcuts import render

# Create your views here.

def inicio_sesion(request):
    return render(request, 'login.html')