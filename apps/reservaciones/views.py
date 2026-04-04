from django.shortcuts import render
from django.utils import timezone
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from apps.boletos.models import Boleto
from .models import Reservacion, AsientoReservacion
from .models import Reservacion

def pagina_reservaciones(request):
    fecha_filtro = request.GET.get('fecha')
    numero_filtro = request.GET.get('numero')
    pasajero_filtro = request.GET.get('pasajero')

    hoy = timezone.now().date()

    reservaciones = Reservacion.objects.select_related(
        'pasajero', 
        'corrida__ruta'
    ).filter(fecha__gte=hoy)

    if fecha_filtro:
        reservaciones = reservaciones.filter(fecha=fecha_filtro)
    
    if numero_filtro:
        reservaciones = reservaciones.filter(corrida__numero__icontains=numero_filtro)
    
    if pasajero_filtro:
        reservaciones = reservaciones.filter(
            Q(pasajero__nombre__icontains=pasajero_filtro) | 
            Q(pasajero__apellPat__icontains=pasajero_filtro)
        )

    total_hoy = Reservacion.objects.filter(fecha=hoy).count()
    total_futuras = Reservacion.objects.filter(fecha__gt=hoy).count()
    total_activas = total_hoy + total_futuras

    context = {
        'reservaciones': reservaciones,
        'total_activas': total_activas,
        'total_hoy': total_hoy,
        'total_futuras': total_futuras,
    }

    return render(request, 'reservaciones.html', context)


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

    # Todos los asientos ligados a esta reservacion
    asientos_ids = AsientoReservacion.objects.filter(
        reservacion=reservacion
    ).values_list('asiento', flat=True)

    # Boletos por corrida + asiento (no por pasajero)
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
    
    

    # Obtenemos la reservación
    reservacion = get_object_or_404(
        Reservacion.objects.select_related('pasajero', 'corrida__ruta__ciudadOrigen', 'corrida__ruta__ciudadDestino', 'corrida__autobus'), 
        numero=reserva_id
    )
    
    # Buscamos todos los boletos asociados a esa corrida y ese pasajero
    boletos = Boleto.objects.filter(
        corrida=reservacion.corrida,
        pasajero=reservacion.pasajero
    ).select_related('asiento', 'tipoPasajero')

    boletos_data = []
    for b in boletos:
        # Calculamos el descuento para el template
        tarifa_base = reservacion.corrida.tarifaBase
        desc_porcentaje = b.tipoPasajero.porcentaje_desc
        monto_descuento = round(float(tarifa_base) * (float(desc_porcentaje) / 100), 2)
        
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
        'es_consulta': True 
    }
    
    # Usamos el mismo template boleto.html que ya tienes
    return render(request, 'boleto.html', context)