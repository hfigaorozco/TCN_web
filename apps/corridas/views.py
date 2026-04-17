from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Corrida, EdoCorrida, CorridaAsiento
from apps.autobuses.models import Autobus, Asiento
from apps.rutas.models import Ruta, Ciudad
from apps.operadores.models import Operador
from django.contrib.auth.decorators import login_required

@login_required
def pagina_corridas(request):
    rutas = Ruta.objects.all()
    operadores = Operador.objects.all()
    autobuses = Autobus.objects.filter(estado__codigo='ACTI')
    ciudades = Ciudad.objects.all()
    estados_corrida = EdoCorrida.objects.all()

    if request.method == 'POST' and 'action' in request.POST:

        if request.POST['action'] == 'agregar_corrida':
            try:
                estado_obj   = EdoCorrida.objects.get(codigo='ACT')
                autobus_obj  = Autobus.objects.get(numero=request.POST.get('autobus'))
                lugares_disp = autobus_obj.cantAsientos
                ruta_obj     = Ruta.objects.get(codigo=request.POST.get('ruta'))
                operador_obj = Operador.objects.get(numero=request.POST.get('operador'))

                fecha_salida = request.POST.get('fecha_salida')
                hora_salida  = request.POST['hora_salida']
                hora_llegada = request.POST['hora_llegada']

                h_salida         = datetime.strptime(hora_salida,  '%H:%M').time()
                h_llegada        = datetime.strptime(hora_llegada, '%H:%M').time()
                fecha_salida_obj = datetime.strptime(fecha_salida, '%Y-%m-%d').date()

                if h_llegada < h_salida:
                    fecha_llegada_obj = fecha_salida_obj + timedelta(days=1)
                else:
                    fecha_llegada_obj = fecha_salida_obj

                operador_ocupado = Corrida.objects.filter(
                    operador=operador_obj,
                    fecha_salida=fecha_salida_obj,
                    estado__codigo='ACT',
                ).filter(
                    hora_salida__lt=h_llegada,
                    hora_llegada__gt=h_salida,
                ).exists()

                if operador_ocupado:
                    messages.error(request, f"El operador {operador_obj.nombre} {operador_obj.apellPat} ya tiene una corrida en ese horario.")
                    return redirect('corridas')

                autobus_ocupado = Corrida.objects.filter(
                    autobus=autobus_obj,
                    fecha_salida=fecha_salida_obj,
                    estado__codigo='ACT',
                ).filter(
                    hora_salida__lt=h_llegada,
                    hora_llegada__gt=h_salida,
                ).exists()

                if autobus_ocupado:
                    messages.error(request, f"El autobús {autobus_obj.numero} ya tiene una corrida en ese horario.")
                    return redirect('corridas')

                nueva_corrida = Corrida.objects.create(
                    hora_salida=hora_salida,
                    fecha_salida=fecha_salida_obj,
                    hora_llegada=hora_llegada,
                    fecha_llegada=fecha_llegada_obj,
                    tarifaBase=request.POST['tarifaBase'],
                    lugaresDisp=lugares_disp,
                    autobus=autobus_obj,
                    ruta=ruta_obj,
                    operador=operador_obj,
                    estado=estado_obj,
                )

                asientos = Asiento.objects.filter(autobus=autobus_obj)
                CorridaAsiento.objects.bulk_create([
                    CorridaAsiento(
                        corrida=nueva_corrida,
                        asiento=asiento,
                        estado=CorridaAsiento.DISPONIBLE,
                    )
                    for asiento in asientos
                ])

                messages.success(request, f"Corrida {nueva_corrida.numero} registrada exitosamente.")

            except Exception as e:
                messages.error(request, f"Error al registrar corrida: {str(e)}")

            return redirect('corridas')

        elif request.POST['action'] == 'editar_corrida':
            try:
                corrida = Corrida.objects.get(numero=request.POST['corrida_numero'])
                corrida.operador_id  = request.POST['edit_operador']
                corrida.autobus_id   = request.POST['edit_autobus']
                corrida.fecha_salida = request.POST['edit_fecha_salida']
                corrida.hora_salida  = request.POST['edit_hora_salida']
                corrida.hora_llegada = request.POST['hora_llegada']
                corrida.fecha_llegada = request.POST['edit_fecha_salida']
                corrida.save()
                messages.success(request, f"Corrida {corrida.numero} actualizada exitosamente.")
            except Exception as e:
                messages.error(request, f"Error al actualizar corrida: {str(e)}")
            return redirect('corridas')

        elif request.POST['action'] == 'cambiar_estado_corrida':
            try:
                corrida = Corrida.objects.get(numero=request.POST['estado_corrida_numero'])
                corrida.estado_id = request.POST['baja_estado']
                corrida.save()
                messages.success(request, f"Corrida {corrida.numero} actualizada exitosamente.")
            except Exception as e:
                messages.error(request, f"Error al cambiar estado: {str(e)}")
            return redirect('corridas')

    corridas = Corrida.objects.select_related(
        'ruta__ciudadOrigen',
        'ruta__ciudadDestino',
        'autobus',
        'operador',
        'estado',
    ).filter(
        fecha_salida__gte=timezone.localdate(),
        estado__codigo='ACT'
    )

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

    ciudad = request.GET.get('filtro_ciudad', '')
    fecha  = request.GET.get('filtro_fecha', '')
    corridas_ciudad_fecha = Corrida.objects.filter(estado__codigo='ACT')

    if ciudad and ciudad != 'todos':
        corridas_ciudad_fecha = corridas_ciudad_fecha.filter(ruta__ciudadOrigen__codigo=ciudad)
    if fecha:
        corridas_ciudad_fecha = corridas_ciudad_fecha.filter(fecha_salida=fecha)
        

    fecha_boletos    = request.GET.get('fecha_boletos', '')
    corridas_boletos = Corrida.objects.filter(estado__codigo='ACT')

    if fecha_boletos:
        corridas_boletos = corridas_boletos.filter(fecha_salida=fecha_boletos)
    for c in corridas_boletos:
        c.asientos_ocupados = c.autobus.cantAsientos - c.lugaresDisp

    context = {
        'operadores':            operadores,
        'rutas':                 rutas,
        'autobuses':             autobuses,
        'corridas':              corridas,
        'ciudades':              ciudades,
        'estados_corrida':       estados_corrida,
        'total_activas':         Corrida.objects.filter(estado__codigo='ACT').count(),
        'total_pasajeros':       CorridaAsiento.objects.filter(estado=CorridaAsiento.OCUPADO).count(),
        'corridas_ciudad_fecha': corridas_ciudad_fecha,
        'corridas_boletos':      corridas_boletos,
    }

    return render(request, 'corridas.html', context)