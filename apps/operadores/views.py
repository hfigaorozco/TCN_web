from django.shortcuts import render, redirect
from .models import Operador
from django.contrib import messages

# Create your views here.

def pagina_operadores(request):
    
    if request.method == 'POST' and 'action' in request.POST:
        
        if request.POST['action'] == 'agregar_operador':
            try:
                Operador.objects.create(
                    nombre = request.POST['nombre'],
                    apellPat = request.POST['apellPat'],
                    apellMat = request.POST['apellMat'],
                    fechaNac = request.POST['fechaNac'],
                    telefono = request.POST['telefono'],
                    fechaContrato = request.POST['fechaContrato'],
                )
            except Exception as e:
                messages.error(request, f"Error al registrar operador: {str(e)}")
            return redirect('operadores')
        
        elif request.POST['action'] == 'editar_operador':
            try:
                operador = Operador.objects.get(numero=request.POST['numero'])
                operador.nombre = request.POST['nombre']
                operador.apellPat = request.POST['apellPat']
                operador.apellMat = request.POST['apellMat']
                operador.telefono = request.POST['telefono']
                operador.save()
            except Exception as e:
                messages.error(request, f"Error al actualizar operador: {str(e)}")
            return redirect('operadores')
    
    operadores = Operador.objects.all()
    numero_operador = request.GET.get('filtro_operador', '')
    
    if numero_operador:
        operadores = operadores.filter(numero__icontains=numero_operador) 
    
    
    operador_seleccionado = None
    operador_numero = request.GET.get('operador_numero')
    
    if operador_numero:
        operador_seleccionado = Operador.objects.filter(numero = operador_numero).first()
    
    context = {
        'operadores': operadores,
        'operador_seleccionado': operador_seleccionado,
    }
    
    return render(request, 'operadores.html', context)

