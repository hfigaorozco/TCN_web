from django.shortcuts import render, redirect
from .models import Corrida, EdoCorrida
from apps.autobuses.models import Autobus
from apps.rutas.models import Ruta, Ciudad
from apps.operadores.models import Operador
# Create your views here.



def pagina_corridas(request):
    rutas = Ruta.objects.all()
    operadores = Operador.objects.all()
    autobuses = Autobus.objects.all()
    ciudades = Ciudad.objects.all()

    
    
    if request.method == 'POST' and 'action' in request.POST:
        if request.POST['action'] == 'agregar_corrida':
            estado_obj = EdoCorrida.objects.get(codigo='ACT')
            autobus_obj = Autobus.objects.get(numero=request.POST.get('autobus'))
            lugares_disponibles = autobus_obj.cantAsientos
            ruta_obj = Ruta.objects.get(codigo=request.POST.get('ruta'))
            operador_obj = Operador.objects.get(numero=request.POST.get('operador'))
            fecha_salida = request.POST.get('fecha_salida')
            
            Corrida.objects.create(
                hora_salida = request.POST['hora_salida'],
                fecha_salida = request.POST['fecha_salida'],
                hora_llegada = request.POST['hora_llegada'],
                fecha_llegada = fecha_salida,
                tarifaBase = request.POST['tarifaBase'],
                lugaresDisp = lugares_disponibles,
                autobus = autobus_obj,
                ruta = ruta_obj,
                operador = operador_obj,
                estado = estado_obj
            )
            return redirect('corridas')
        
        elif request.POST['action'] == 'editar_corrida':
            corrida = Corrida.objects.get(numero=request.POST['corrida_numero'])
            corrida.operador_id = request.POST['edit_operador']
            corrida.autobus_id = request.POST['edit_autobus']
            corrida.fecha_salida = request.POST['edit_fecha_salida']
            corrida.hora_salida = request.POST['edit_hora_salida']
            corrida.hora_llegada = request.POST['hora_llegada']
            corrida.fecha_llegada = request.POST['edit_fecha_salida']
            corrida.save()
            return redirect('corridas') 
        
        elif request.POST['action'] == 'cambiar_estado_corrida':
            corrida = Corrida.objects.get(numero=request.POST['estado_corrida_numero'])
            corrida.estado_id = request.POST['baja_estado']
            corrida.save()
            return redirect('corridas')
            
    
    corridas = Corrida.objects.filter(estado__codigo = 'ACT')
    numero_corrida = request.GET.get('filtro_corrida', '')
    origen = request.GET.get('filtro_origen', '')
    destino = request.GET.get('filtro_destino', '')
    estados_corrida = EdoCorrida.objects.all()
    
    if numero_corrida and origen == 'todos' and destino == 'todos':
        corridas = corridas.filter(numero__icontains=numero_corrida)  
    if numero_corrida:
        corridas = corridas.filter(numero__icontains=numero_corrida)  
    if origen and origen != 'todos':
        corridas = corridas.filter(ruta__ciudadOrigen__codigo=origen)
    if destino and destino != 'todos':
        corridas = corridas.filter(ruta__ciudadDestino__codigo=destino)
        
    context ={
        'operadores': operadores,
        'rutas': rutas,
        'autobuses': autobuses,
        'corridas': corridas,
        'ciudades': ciudades,
        'estados_corrida': estados_corrida
    }
    
    return render(request, 'corridas.html', context)