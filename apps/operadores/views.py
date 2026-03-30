from django.shortcuts import render, redirect
from .models import Operador

# Create your views here.

def pagina_operadores(request):
    
    if request.method == 'POST' and 'action' in request.POST:
        
        if request.POST['action'] == 'agregar_operador':
            
            Operador.objects.create(
                nombre = request.POST['nombre'],
                apellPat = request.POST['apellPat'],
                apellMat = request.POST['apellMat'],
                fechaNac = request.POST['fechaNac'],
                telefono = request.POST['telefono'],
                fechaContrato = request.POST['fechaContrato'],
            )
            return redirect('operadores')
    
    operadores = Operador.objects.all()
    
    return render(request, 'operadores.html', {'operadores': operadores})

