from django.shortcuts import render, redirect
from .models import Autobus, Marca, Modelo, TipoAutobus, EdoAutobus, Asiento


def generar_asientos(autobus_obj):
    tipo = autobus_obj.tipoAutobus_id  # 'PLUS' o 'PLAT'

    if tipo == 'PLUS':
        total_filas = 10   
        extra = [41, 42, 43, 44]
    elif tipo == 'PLAT':
        total_filas = 9    
        extra = []
    else:
        return

    asientos = []

    for col in range(total_filas):
        base = col * 4
        grupo = [
            (base + 1, 'VENTANA'),  
            (base + 2, 'PASILLO'), 
            (base + 3, 'PASILLO'),  
            (base + 4, 'VENTANA'), 
        ]
        asientos.extend(grupo)

    ubicaciones_extra = {
        41: 'VENTANA',
        42: 'VENTANA',
        43: 'PASILLO',
        44: 'PASILLO',
    }
    for num in extra:
        asientos.append((num, ubicaciones_extra[num]))


    for numero, ubicacion in asientos:
        clave = f"{autobus_obj.numero}-{numero:02d}"  
        Asiento.objects.create(
            clave=clave,
            numero=numero,
            ubicacion=ubicacion,
            autobus=autobus_obj,
        )


def pagina_autobuses(request):
    error = None

    if request.method == 'POST' and 'action' in request.POST:

        if request.POST['action'] == 'agregar_autobus':
            tipo_codigo = request.POST['tipoAutobus']
            asientos_por_tipo = {'PLUS': 44, 'PLAT': 36}
            cant_asientos = asientos_por_tipo.get(tipo_codigo, 0)

            # Corrección: manejo seguro de claveWIFI
            wifi = request.POST.get('claveWIFI', '').strip()
            clave_wifi = wifi.upper() if wifi else None

            autobus = Autobus.objects.create(
                numero=int(request.POST['numero']),
                matricula=request.POST['matricula'].upper(),
                claveWIFI=clave_wifi,
                cantAsientos=cant_asientos,
                tipoAutobus=TipoAutobus.objects.get(codigo=tipo_codigo),
                estado=EdoAutobus.objects.get(codigo='ACTI'),
                marca=Marca.objects.get(clave=request.POST['marca']),
                modelo=Modelo.objects.get(clave=request.POST['modelo']),
            )

            # Registrar asientos automáticamente
            generar_asientos(autobus)

            return redirect('autobuses')

        elif request.POST['action'] == 'baja_autobus':
            pass

    autobuses = Autobus.objects.filter(estado__codigo='ACTI')
    context = {
        'autobuses': autobuses,
        'marcas': Marca.objects.all(),
        'modelos': Modelo.objects.all(),
        'tipos_autobus': TipoAutobus.objects.all(),
        'total_activos': autobuses.count(),
        'total_disponibles': autobuses.filter(estado__descripcion='Disponible').count(),
        'total_en_ruta': autobuses.filter(estado__descripcion='En Ruta').count(),
        'error': error,
    }
    return render(request, 'autobuses.html', context)