from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from apps.corridas.models import Corrida
from apps.rutas.models import Ciudad
from apps.reservaciones.models import Reservacion, AsientoReservacion
from datetime import datetime, date, timedelta

def index(request):
    
    corridas_list = Corrida.objects.filter(
        fecha_salida__gte=date.today()
    ).order_by('fecha_salida', 'hora_salida')
    
    corridas_data = []
    now = datetime.now()

    for c in corridas_list:
       
        dt_salida = datetime.combine(c.fecha_salida, c.hora_salida)
        dt_llegada = datetime.combine(c.fecha_llegada, c.hora_llegada)
        
        # para los estados dinamicos de las corridas
        if now > dt_llegada:
            estado_texto = "Finalizada"
            estado_clase = "finalizada"
        elif now > dt_salida:
            estado_texto = "En curso"
            estado_clase = "en-curso"
        elif dt_salida - now <= timedelta(hours=1):
            estado_texto = "Próxima"
            estado_clase = "proxima"
        else:
            estado_texto = "Pendiente"
            estado_clase = "pendiente"

        corridas_data.append({
            'id': c.numero,
            'hora': c.hora_salida.strftime('%H:%M'),
            'fecha': c.fecha_salida.strftime('%Y-%m-%d'),
            'origen': c.ruta.ciudadOrigen.nombre,
            'destino': c.ruta.ciudadDestino.nombre,
            'estado': estado_texto,
            'estado_clase': estado_clase,
            'autobus': f'#{c.autobus.numero} - {c.autobus.matricula}',
        })

    
    meses_filtro = []
    nombres_meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", 
                      "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
    
    today = date.today()
    for i in range(6):
        
        month = (today.month + i - 1) % 12 + 1
        year = today.year + (today.month + i - 1) // 12
        
        meses_filtro.append({
            'nombre': f"{nombres_meses[month - 1]} {year}",
            'valor': f"{year}-{month:02d}"
        })

    detalle = None
    pasajeros_data = []
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
        
       
        reservaciones = Reservacion.objects.filter(corrida=c).select_related('pasajero')
        for res in reservaciones:
            asientos_res = AsientoReservacion.objects.filter(reservacion=res).select_related('asiento')
            for ar in asientos_res:
                pasajeros_data.append({
                    'asiento': ar.asiento.numero,
                    'nombre': f"{res.pasajero.nombre} {res.pasajero.apellPat} {res.pasajero.apellMat or ''}".strip(),
                    'tipo': 'Normal',
                    'estado': 'confirmado'
                })

    context = {
        'corridas': corridas_data,
        'pasajeros': pasajeros_data,
        'ciudades': Ciudad.objects.all(),
        'meses_filtro': meses_filtro,
        'detalle': detalle,
    }

    return render(request, 'index.html', context)

def get_corrida_details(request, corrida_id):
    corrida = get_object_or_404(Corrida, numero=corrida_id)
    
    total_asientos = corrida.autobus.cantAsientos
    ocupados = total_asientos - corrida.lugaresDisp
    porcentaje = int((ocupados / total_asientos) * 100) if total_asientos > 0 else 0
    
    detalle = {
        'autobus': corrida.autobus.numero,
        'tipo': corrida.autobus.tipoAutobus.descripcion,
        'operador': f"{corrida.operador.nombre} {corrida.operador.apellPat}",
        'ruta': f"{corrida.ruta.ciudadOrigen.nombre} → {corrida.ruta.ciudadDestino.nombre}",
        'salida': corrida.hora_salida.strftime('%H:%M'),
        'ocupados': ocupados,
        'capacidad': total_asientos,
        'porcentaje': porcentaje
    }
    
  
    reservaciones = Reservacion.objects.filter(corrida=corrida).select_related('pasajero')
    pasajeros = []
    for res in reservaciones:
        asientos_res = AsientoReservacion.objects.filter(reservacion=res).select_related('asiento')
        for ar in asientos_res:
            pasajeros.append({
                'asiento': ar.asiento.numero,
                'nombre': f"{res.pasajero.nombre} {res.pasajero.apellPat} {res.pasajero.apellMat or ''}".strip(),
                'tipo': 'Normal',
                'estado': 'confirmado'
            })
        
    return JsonResponse({
        'detalle': detalle,
        'pasajeros': pasajeros
    })
