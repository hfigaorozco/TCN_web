from django.shortcuts import render
from django.db import connection
from apps.corridas.models import Corrida
from apps.rutas.models import Ciudad


def index(request):
    # Fetch corridas
    corridas_list = Corrida.objects.all().order_by('fecha_salida', 'hora_salida')[:10]

    corridas_data = []
    for c in corridas_list:
        corridas_data.append({
            'hora': c.hora_salida.strftime('%H:%M'),
            'origen': c.ruta.ciudadOrigen.nombre,
            'destino': c.ruta.ciudadDestino.nombre,
            'estado': c.estado.descripcion.lower(),
            'autobus': f'#{c.autobus.numero} - {c.autobus.matricula}',
        })

    # Consulta SQL directa para mostrar todos los pasajeros
    pasajeros_data = []
    with connection.cursor() as cursor:
        cursor.execute("SELECT nombre, apellPat FROM pasajero")
        rows = cursor.fetchall()
        for row in rows:
            pasajeros_data.append({
                'asiento': 'A1',
                'nombre': f"{row[0]} {row[1]}",
                'tipo': 'Adulto',
                'estado': 'confirmado'
            })

    # Detalles de la primera corrida si existe
    detalle = None
    if corridas_list.exists():
        c = corridas_list[0]
        total_asientos = c.autobus.cantAsientos
        ocupados = total_asientos - c.lugaresDisp
        porcentaje = int((ocupados / total_asientos) * 100) if total_asientos > 0 else 0

        detalle = {
            'autobus': c.autobus.numero,
            'tipo': c.autobus.tipoAutobus.descripcion,
            'operador': f"{c.operador.nombre} {c.operador.apellPat}",
            'ruta': f"{c.ruta.ciudadOrigen.nombre} → {c.ruta.ciudadDestino.nombre}",
            'salida': c.hora_salida.strftime('%H:%M'),
            'ocupados': ocupados,
            'capacidad': total_asientos,
            'porcentaje': porcentaje
        }

    context = {
        'corridas': corridas_data,
        'pasajeros': pasajeros_data,
        'ciudades': Ciudad.objects.all(),
        'detalle': detalle,
    }

    return render(request, 'index.html', context)