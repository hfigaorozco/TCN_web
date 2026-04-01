from django.shortcuts import render
from django.utils import timezone
from apps.corridas.models import Corrida
from apps.rutas.models import Ciudad


def buscar_corridas(request):
    corridas = []
    sin_resultados = False
    ciudades = Ciudad.objects.all()

    origen    = request.GET.get('origen', '')
    destino   = request.GET.get('destino', '')
    fecha     = request.GET.get('fecha', '')
    pasajeros = request.GET.get('pasajeros', '')

    # Obtener nombres de las ciudades
    origen_nombre  = ''
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
        'corridas':        corridas,
        'ciudades':        ciudades,
        'sin_resultados':  sin_resultados,
        'origen':          origen,
        'destino':         destino,
        'origen_nombre':   origen_nombre,
        'destino_nombre':  destino_nombre,
        'fecha':           fecha,
        'pasajeros':       pasajeros,
    }
    return render(request, 'comprarboleto.html', context)