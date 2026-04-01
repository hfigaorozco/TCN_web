from django.shortcuts import render
from .models import Corrida, EdoCorrida
from apps.autobuses.models import Autobus
from apps.rutas.models import Ruta
from apps.operadores.models import Operador
# Create your views here.



def pagina_corridas(request):
    rutas = Ruta.objects.all()
    operadores = Operador.objects.all()
    autobuses = Autobus.objects.all()
    

    
    
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
    
    corridas = Corrida.objects.all()
    numero_corrida = request.GET.get('filtro_corrida', '')
    origen = request.GET.get('filtro_origen', '')
    destino = request.GET.get('filtro_destino', '')
    
    if numero_corrida:
        corridas = corridas.filter(numero_icontains=numero_corrida)
        
    if origen and origen != 'todos':
        corridas = corridas.filter(ruta__ciudadOrigen_icontains=origen)
    
    if destino and destino != 'todos':
        corridas = corridas.filter(ruta__ciudadDestino_icontains=destino)
        
    context ={
        'operadores': operadores,
        'rutas': rutas,
        'autobuses': autobuses,
        'corridas': corridas,
    }
    
    return render(request, 'corridas.html', context)