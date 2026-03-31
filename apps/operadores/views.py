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
    numero_operador = request.GET.get('filtro_operador', '')
    
    if numero_operador:
        operadores = operadores.filter(numero__icontains=numero_operador) 
    
    
    operador_seleccionado = None
    operador_numero = request.GET.get('operador_numero')
    
    if operador_numero:
        operador_seleccionado = Operador.objects.filter(numero = operador_numero).first()
    
    return render(request, 'operadores.html', {'operadores': operadores})

