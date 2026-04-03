from django.shortcuts import render
from django.utils import timezone
from .models import Reservacion
from django.db.models import Q

def pagina_reservaciones(request):
    # 1. Obtener parámetros
    fecha_filtro = request.GET.get('fecha')
    numero_filtro = request.GET.get('numero')
    pasajero_filtro = request.GET.get('pasajero')

    # 2. Queryset base
    reservaciones = Reservacion.objects.select_related('pasajero', 'corrida__ruta').all()

    # 3. Aplicar lógica de filtrado
    if fecha_filtro:
        reservaciones = reservaciones.filter(fecha=fecha_filtro)
    
    if numero_filtro:
        reservaciones = reservaciones.filter(corrida__numero__icontains=numero_filtro)
    
    if pasajero_filtro:
        # Filtra por nombre o apellido
        reservaciones = reservaciones.filter(
            Q(pasajero__nombre__icontains=pasajero_filtro) | 
            Q(pasajero__apellPat__icontains=pasajero_filtro)
        )

    # --- LÓGICA DE LOS CARDS (Se mantiene igual) ---
    hoy = timezone.now().date()
    total_activas = Reservacion.objects.filter(fechaLimPago__gte=hoy).count()
    total_hoy = Reservacion.objects.filter(fecha=hoy).count()
    total_futuras = Reservacion.objects.filter(fecha__gt=hoy).count()

    context = {
        'reservaciones': reservaciones,
        'total_activas': total_activas,
        'total_hoy': total_hoy,
        'total_futuras': total_futuras,
    }

    return render(request, 'reservaciones.html', context)