from django.shortcuts import render, redirect
from .models import Corrida, EdoCorrida, CorridaAsiento
from apps.autobuses.models import Autobus, Asiento
from apps.rutas.models import Ruta, Ciudad
from apps.operadores.models import Operador


def pagina_corridas(request):
    rutas           = Ruta.objects.all()
    operadores      = Operador.objects.all()
    autobuses       = Autobus.objects.filter(estado__codigo='ACTI')
    ciudades        = Ciudad.objects.all()
    estados_corrida = EdoCorrida.objects.all()

    if request.method == 'POST' and 'action' in request.POST:
        if request.POST['action'] == 'agregar_corrida':
            estado_obj   = EdoCorrida.objects.get(codigo='ACT')
            autobus_obj  = Autobus.objects.get(numero=request.POST.get('autobus'))
            lugares_disp = autobus_obj.cantAsientos
            ruta_obj     = Ruta.objects.get(codigo=request.POST.get('ruta'))
            operador_obj = Operador.objects.get(numero=request.POST.get('operador'))
            fecha_salida = request.POST.get('fecha_salida')

            corrida = Corrida.objects.create(
                hora_salida   = request.POST['hora_salida'],
                fecha_salida  = fecha_salida,
                hora_llegada  = request.POST['hora_llegada'],
                fecha_llegada = fecha_salida,
                tarifaBase    = request.POST['tarifaBase'],
                lugaresDisp   = lugares_disp,
                autobus       = autobus_obj,
                ruta          = ruta_obj,
                operador      = operador_obj,
                estado        = estado_obj,
            )

            # Generar corrida_asiento para cada asiento del autobús asignado
            # Los asientos ya existen gracias a generar_asientos() en autobuses
            asientos = Asiento.objects.filter(autobus=autobus_obj)
            CorridaAsiento.objects.bulk_create([
                CorridaAsiento(
                    corrida=corrida,
                    asiento=asiento,
                    estado=CorridaAsiento.DISPONIBLE,
                )
                for asiento in asientos
            ])

            return redirect('corridas')

    corridas = Corrida.objects.select_related(
        'ruta__ciudadOrigen',
        'ruta__ciudadDestino',
        'autobus',
        'operador',
        'estado',
    ).all()

    numero_corrida = request.GET.get('filtro_corrida', '')
    origen         = request.GET.get('filtro_origen', '')
    destino        = request.GET.get('filtro_destino', '')

    if numero_corrida:
        corridas = corridas.filter(numero__icontains=numero_corrida)
    if origen and origen != 'todos':
        corridas = corridas.filter(ruta__ciudadOrigen__codigo=origen)
    if destino and destino != 'todos':
        corridas = corridas.filter(ruta__ciudadDestino__codigo=destino)

    for corrida in corridas:
        corrida.pasajeros_count = CorridaAsiento.objects.filter(
            corrida=corrida,
            estado=CorridaAsiento.OCUPADO,
        ).count()

    context = {
        'operadores':          operadores,
        'rutas':               rutas,
        'autobuses':           autobuses,
        'corridas':            corridas,
        'ciudades':            ciudades,
        'estados_corrida':     estados_corrida,
        'total_activas':       Corrida.objects.filter(estado__codigo='ACT').count(),
        'total_pasajeros':     CorridaAsiento.objects.filter(estado=CorridaAsiento.OCUPADO).count(),
        'corridas_fecha_ciudad': [],
        'corridas_boletos':    [],
    }

    return render(request, 'corridas.html', context)