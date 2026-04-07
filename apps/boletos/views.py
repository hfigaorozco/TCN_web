import json
from datetime import date
from django.shortcuts import render, redirect, get_object_or_404
from .models import Boleto
from apps.corridas.models import Corrida, CorridaAsiento
from apps.reservaciones.models import Reservacion, AsientoReservacion
from apps.autobuses.models import Asiento
from apps.rutas.models import Ciudad
from apps.pasajeros.models import Pasajero, TipoPasajero
from django.contrib.auth.decorators import login_required

# BUSCAR CORRIDAS 

@login_required
def buscar_corridas(request):
    corridas = []
    sin_resultados = False
    ciudades = Ciudad.objects.all()

    origen = request.GET.get('origen', '')
    destino = request.GET.get('destino', '')
    fecha = request.GET.get('fecha', '')
    pasajeros = request.GET.get('pasajeros', '')

    origen_nombre = ''
    destino_nombre = ''

    if origen:
        try:
            origen_nombre = Ciudad.objects.get(codigo=origen).nombre
        except Ciudad.DoesNotExist:
            pass

    if destino:
        try:
            destino_nombre = Ciudad.objects.get(codigo=destino).nombre
        except Ciudad.DoesNotExist:
            pass

    if origen and destino and fecha and pasajeros:
        try:
            pasajeros_int = int(pasajeros)
            corridas = Corrida.objects.filter(
                ruta__ciudadOrigen__codigo=origen,
                ruta__ciudadDestino__codigo=destino,
                fecha_salida=fecha,
                lugaresDisp__gte=pasajeros_int,
                estado__codigo='ACT',
            ).select_related(
                'ruta__ciudadOrigen',
                'ruta__ciudadDestino',
                'autobus__tipoAutobus',
            ).order_by('hora_salida')

            if not corridas:
                sin_resultados = True

        except (ValueError, Exception):
            sin_resultados = True

    context = {
        'corridas': corridas,
        'ciudades': ciudades,
        'sin_resultados': sin_resultados,
        'origen': origen,
        'destino': destino,
        'origen_nombre': origen_nombre,
        'destino_nombre': destino_nombre,
        'fecha': fecha,
        'pasajeros': pasajeros,
    }
    return render(request, 'comprarboleto.html', context)


# Mapa de los asientos de cada autobus

@login_required
def seleccionar_asiento(request, corrida_id):
    corrida = Corrida.objects.select_related(
        'autobus__tipoAutobus',
        'ruta__ciudadOrigen',
        'ruta__ciudadDestino',
    ).get(numero=corrida_id)

    pasajeros = int(request.GET.get('pasajeros', 1))
    origen = request.GET.get('origen', '')
    destino = request.GET.get('destino', '')
    fecha = request.GET.get('fecha', '')

    corrida_asientos = CorridaAsiento.objects.filter(
        corrida=corrida
    ).select_related('asiento')

    estado_asientos = {
        ca.asiento.numero: ca.estado
        for ca in corrida_asientos
    }

    tipos_pasajero = TipoPasajero.objects.all()
    tipo_bus = corrida.autobus.tipoAutobus.codigo

    template = (
        'seleccion-asiento-plus.html'
        if tipo_bus == 'PLUS'
        else 'seleccion-asiento-platino.html'
    )

    context = {
        'corrida': corrida,
        'pasajeros': pasajeros,
        'estado_asientos': json.dumps(estado_asientos),
        'tipos_pasajero': tipos_pasajero,
        'origen': origen,
        'destino': destino,
        'fecha': fecha,
    }
    return render(request, template, context)


# Confirmacion de la compra

@login_required
def confirmacion_compra(request):
    if request.method == 'POST':
        corrida_id = request.POST.get('corrida_id')
        pasajeros_json = request.POST.get('pasajeros_data')
        origen = request.POST.get('origen', '')
        destino = request.POST.get('destino', '')

        corrida = Corrida.objects.select_related(
            'autobus__tipoAutobus',
            'ruta__ciudadOrigen',
            'ruta__ciudadDestino',
        ).get(numero=corrida_id)

        pasajeros_data = json.loads(pasajeros_json)

        IVA_RATE = 0.16
        subtotal = 0

        for p in pasajeros_data:
            tipo = TipoPasajero.objects.get(codigo=p['tipo_pasajero'])
            descuento = corrida.tarifaBase * (tipo.porcentaje_desc / 100)
            precio = corrida.tarifaBase - descuento
            p['precio'] = round(precio, 2)
            p['tipo_descripcion'] = tipo.descripcion
            p['descuento'] = round(descuento, 2)
            subtotal += precio

        iva = round(subtotal * IVA_RATE, 2)
        total = round(subtotal + iva, 2)

        request.session['compra_pendiente'] = {
            'corrida_id': corrida_id,
            'pasajeros_data': pasajeros_data,
            'subtotal': round(subtotal, 2),
            'iva': iva,
            'total': total,
            'origen': origen,
            'destino': destino,
        }

        context = {
            'corrida': corrida,
            'pasajeros_data': pasajeros_data,
            'subtotal': round(subtotal, 2),
            'iva': iva,
            'total': total,
            'cant_pasajeros': len(pasajeros_data),
        }
        return render(request, 'confirmacion-compra.html', context)

    return redirect('index')


# Generar los boletos

@login_required
def generar_boletos(request):
    if request.method != 'POST':
        return redirect('index')

    compra = request.session.get('compra_pendiente')
    if not compra:
        return redirect('index')

    corrida = Corrida.objects.select_related(
        'autobus__tipoAutobus',
        'ruta__ciudadOrigen',
        'ruta__ciudadDestino',
    ).get(numero=compra['corrida_id'])

    hoy = date.today()
    fecha_lim = corrida.fecha_salida
    IVA_RATE = 0.16
    pasajeros_data = compra['pasajeros_data']
    cant = len(pasajeros_data)
    boletos_generados = []

    pasajeros_objs = []
    for p in pasajeros_data:
        nombre_parts = p['nombre'].strip().split()
        nombre = nombre_parts[0] if nombre_parts else p['nombre']
        apellidos = p['apellidos'].strip().split()
        apell_pat = apellidos[0] if apellidos else ''
        apell_mat = apellidos[1] if len(apellidos) > 1 else ''

        pasajero_obj = Pasajero.objects.create(
            nombre = nombre,
            apellPat = apell_pat,
            apellMat = apell_mat,
            edad = int(p['edad']),
        )
        pasajeros_objs.append(pasajero_obj)

    reservacion = Reservacion.objects.create(
        fecha = hoy,
        fechaLimPago = fecha_lim,
        cantPasajeros = cant,
        subtotal = compra['subtotal'],
        IVA = compra['iva'],
        total = compra['total'],
        pasajero = pasajeros_objs[0],
        corrida = corrida,
    )

    for p, pasajero_obj in zip(pasajeros_data, pasajeros_objs):
        tipo_obj = TipoPasajero.objects.get(codigo=p['tipo_pasajero'])
        asiento_obj = Asiento.objects.get(
            numero = int(p['asiento']),
            autobus = corrida.autobus,
        )

        AsientoReservacion.objects.create(
            asiento = asiento_obj,
            reservacion = reservacion,
        )

        boleto = Boleto.objects.create(
            precio = p['precio'],
            asiento = asiento_obj,
            pasajero = pasajero_obj,
            tipoPasajero = tipo_obj,
            corrida = corrida,
        )

        CorridaAsiento.objects.filter(
            corrida = corrida,
            asiento = asiento_obj,
        ).update(estado=CorridaAsiento.OCUPADO)

        boletos_generados.append({
            'boleto': boleto,
            'reservacion': reservacion,
            'pasajero': pasajero_obj,
            'tipo': tipo_obj,
            'descuento': round(corrida.tarifaBase*(tipo_obj.porcentaje_desc/100), 2),
        })

    corrida.lugaresDisp-=cant
    corrida.save()

    del request.session['compra_pendiente']

    context = {
        'corrida':           corrida,
        'boletos_generados': boletos_generados,
        'total_general':     compra['total'],
    }
    return render(request, 'boleto.html', context)


# Ver boletos desde modulo de reservaciones

@login_required
def ver_boletos(request, reserva_id):
    reservacion = get_object_or_404(
        Reservacion.objects.select_related(
            'pasajero',
            'corrida__ruta__ciudadOrigen',
            'corrida__ruta__ciudadDestino',
            'corrida__autobus__tipoAutobus',
        ),
        numero=reserva_id
    )

    asientos_reservacion = AsientoReservacion.objects.filter(
        reservacion=reservacion
    ).values_list('asiento', flat=True)

    boletos = Boleto.objects.filter(
        corrida=reservacion.corrida,
        asiento__in=asientos_reservacion,
    ).select_related('asiento', 'pasajero', 'tipoPasajero')

    boletos_data = []
    for b in boletos:
        tarifa_base = reservacion.corrida.tarifaBase
        desc_porcentaje = b.tipoPasajero.porcentaje_desc
        monto_descuento = round(tarifa_base * (desc_porcentaje / 100), 2)

        boletos_data.append({
            'boleto': b,
            'reservacion': reservacion,
            'pasajero': b.pasajero,
            'tipo': b.tipoPasajero,
            'descuento': monto_descuento,
        })

    context = {
        'corrida': reservacion.corrida,
        'boletos_generados': boletos_data,
        'total_general': reservacion.total,
        'es_consulta': True,
    }

    return render(request, 'boleto.html', context)