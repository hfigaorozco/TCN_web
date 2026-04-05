from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from apps.corridas.models import Corrida
from apps.rutas.models import Ciudad
from apps.boletos.models import Boleto 
from datetime import datetime, date
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.utils import timezone


@login_required
def index(request):

    corridas_list = Corrida.objects.filter(
        fecha_salida__gte=date.today()
    ).order_by('fecha_salida', 'hora_salida')

    corridas_data = []
    now = timezone.localtime()

    for c in corridas_list:
        dt_salida = timezone.make_aware(
            datetime.combine(c.fecha_salida, c.hora_salida)
        )
        dt_llegada = timezone.make_aware(
            datetime.combine(c.fecha_llegada, c.hora_llegada)
        )

        # prioridad: estado en BD
        if c.estado.codigo == 'INA':
            estado_texto = "Cancelada"
            estado_clase = "cancelada"
        else:
            if now < dt_salida:
                estado_texto = "Próxima"
                estado_clase = "proxima"

            elif dt_salida <= now <= dt_llegada:
                estado_texto = "En curso"
                estado_clase = "en-curso"

            else:
                estado_texto = "Finalizada"
                estado_clase = "finalizada"

        corridas_data.append({
            'id':          c.numero,
            'hora':        c.hora_salida.strftime('%H:%M'),
            'fecha':       c.fecha_salida.strftime('%Y-%m-%d'),
            'origen':      c.ruta.ciudadOrigen.nombre,
            'destino':     c.ruta.ciudadDestino.nombre,
            'estado':      estado_texto,
            'estado_clase': estado_clase,
            'autobus':     f'#{c.autobus.numero} - {c.autobus.matricula}',
        })

    # FILTRO DE FECHAS 
    nombres_dias = [
        'Lunes', 'Martes', 'Miércoles', 'Jueves',
        'Viernes', 'Sábado', 'Domingo'
    ]
    nombres_meses = [
        'enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio',
        'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre'
    ]

    fechas_qs = (
        Corrida.objects
        .filter(fecha_salida__gte=date.today())
        .values_list('fecha_salida', flat=True)
        .distinct()
        .order_by('fecha_salida')
    )

    dias_filtro = []
    for f in fechas_qs:
        dias_filtro.append({
            'valor': f.strftime('%Y-%m-%d'),
            'nombre': f"{nombres_dias[f.weekday()]} {f.day} de {nombres_meses[f.month - 1]} de {f.year}"
        })

    # DETALLE PRIMERA CORRIDA 
    detalle = None
    pasajeros_data = []

    if corridas_list.exists():
        c = corridas_list[0]

        total_asientos = c.autobus.cantAsientos
        ocupados       = total_asientos - c.lugaresDisp
        porcentaje     = int((ocupados / total_asientos) * 100) if total_asientos > 0 else 0

        detalle = {
            'autobus':    c.autobus.numero,
            'tipo':       c.autobus.tipoAutobus.descripcion,
            'operador':   f"{c.operador.nombre} {c.operador.apellPat}",
            'ruta':       f"{c.ruta.ciudadOrigen.nombre} - {c.ruta.ciudadDestino.nombre}",
            'salida':     c.hora_salida.strftime('%H:%M'),
            'ocupados':   ocupados,
            'capacidad':  total_asientos,
            'porcentaje': porcentaje,
        }

        boletos = Boleto.objects.filter(
            corrida=c
        ).select_related('pasajero', 'asiento', 'tipoPasajero')

        for b in boletos:
            pasajeros_data.append({
                'asiento': b.asiento.numero,
                'nombre': f"{b.pasajero.nombre} {b.pasajero.apellPat} {b.pasajero.apellMat or ''}".strip(),
                'tipo': b.tipoPasajero.descripcion,
                'estado': 'confirmado',
            })

    context = {
        'corridas':    corridas_data,
        'pasajeros':   pasajeros_data,
        'ciudades':    Ciudad.objects.all(),
        'dias_filtro': dias_filtro,
        'detalle':     detalle,
    }

    return render(request, 'index.html', context)


@login_required
def get_corrida_details(request, corrida_id):
    corrida = get_object_or_404(Corrida, numero=corrida_id)

    total_asientos = corrida.autobus.cantAsientos
    ocupados       = total_asientos - corrida.lugaresDisp
    porcentaje     = int((ocupados / total_asientos) * 100) if total_asientos > 0 else 0

    detalle = {
        'autobus':    corrida.autobus.numero,
        'tipo':       corrida.autobus.tipoAutobus.descripcion,
        'operador':   f"{corrida.operador.nombre} {corrida.operador.apellPat}",
        'ruta':       f"{corrida.ruta.ciudadOrigen.nombre} → {corrida.ruta.ciudadDestino.nombre}",
        'salida':     corrida.hora_salida.strftime('%H:%M'),
        'ocupados':   ocupados,
        'capacidad':  total_asientos,
        'porcentaje': porcentaje,
    }

    boletos = Boleto.objects.filter(
        corrida=corrida
    ).select_related('pasajero', 'asiento', 'tipoPasajero')

    pasajeros = []
    for b in boletos:
        pasajeros.append({
            'asiento': b.asiento.numero,
            'nombre': f"{b.pasajero.nombre} {b.pasajero.apellPat} {b.pasajero.apellMat or ''}".strip(),
            'tipo': b.tipoPasajero.descripcion,
            'estado': 'confirmado',
        })

    return JsonResponse({
        'detalle':   detalle,
        'pasajeros': pasajeros,
    })


@login_required
def cambiar_contrasena(request):
    if request.method == 'POST':
        actual = request.POST.get('password_actual', '')
        nueva  = request.POST.get('password_nueva', '')

        if not request.user.check_password(actual):
            return JsonResponse({'ok': False, 'error': 'La contraseña actual es incorrecta'})

        if len(nueva) < 8:
            return JsonResponse({'ok': False, 'error': 'La nueva contraseña debe tener al menos 8 caracteres'})

        request.user.set_password(nueva)
        request.user.save()
        update_session_auth_hash(request, request.user)

        return JsonResponse({'ok': True})

    return JsonResponse({'ok': False, 'error': 'Método no permitido'})