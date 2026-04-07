from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.db.models import Q
from apps.boletos.models import Boleto
from .models import Reservacion, AsientoReservacion
from django.contrib.auth.decorators import login_required

@login_required
def pagina_reservaciones(request):
    hoy = timezone.localdate()

    fecha_filtro    = request.GET.get('fecha')
    numero_filtro   = request.GET.get('numero')
    pasajero_filtro = request.GET.get('pasajero')

    reservaciones = Reservacion.objects.select_related(
        'pasajero',
        'corrida__ruta__ciudadOrigen',
        'corrida__ruta__ciudadDestino',
    ).filter(corrida__fecha_salida__gte=hoy).order_by('corrida__fecha_salida')

    if fecha_filtro:
        reservaciones = reservaciones.filter(corrida__fecha_salida=fecha_filtro)

    if numero_filtro:
        reservaciones = reservaciones.filter(numero=numero_filtro)

    if pasajero_filtro:
        reservaciones = reservaciones.filter(
            Q(pasajero__nombre__icontains=pasajero_filtro) |
            Q(pasajero__apellPat__icontains=pasajero_filtro)
        )

    total_hoy     = Reservacion.objects.filter(fecha=hoy).count()
    total_futuras = Reservacion.objects.filter(corrida__fecha_salida__gt=hoy).count()
    total_activas = total_hoy + total_futuras

    context = {
        'reservaciones': reservaciones,
        'total_activas': total_activas,
        'total_hoy':     total_hoy,
        'total_futuras': total_futuras,
        'fecha_filtro':  fecha_filtro or str(hoy),
    }

    return render(request, 'reservaciones.html', context)

@login_required
def ver_boletos_reserva(request, reserva_id):
    reservacion = get_object_or_404(
        Reservacion.objects.select_related(
            'pasajero',
            'corrida__ruta__ciudadOrigen',
            'corrida__ruta__ciudadDestino',
            'corrida__autobus__tipoAutobus',
        ),
        numero=reserva_id
    )

    asientos_ids = AsientoReservacion.objects.filter(
        reservacion=reservacion
    ).values_list('asiento', flat=True)

    boletos = Boleto.objects.filter(
        corrida=reservacion.corrida,
        asiento__in=asientos_ids,
    ).select_related('asiento', 'pasajero', 'tipoPasajero')

    boletos_data = []
    for b in boletos:
        tarifa_base     = reservacion.corrida.tarifaBase
        desc_porcentaje = b.tipoPasajero.porcentaje_desc
        monto_descuento = round(float(tarifa_base) * (float(desc_porcentaje) / 100), 2)

        boletos_data.append({
            'boleto':      b,
            'reservacion': reservacion,
            'pasajero':    b.pasajero,
            'tipo':        b.tipoPasajero,
            'descuento':   monto_descuento,
        })

    context = {
        'corrida':           reservacion.corrida,
        'boletos_generados': boletos_data,
        'total_general':     reservacion.total,
        'es_consulta':       True,
    }

    return render(request, 'boleto.html', context)