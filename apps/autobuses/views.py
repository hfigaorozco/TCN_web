from django.shortcuts import render, redirect
from django.db import IntegrityError
from .models import Autobus, Marca, Modelo, TipoAutobus, EdoAutobus, Asiento


def generar_asientos(autobus_obj):
    tipo = autobus_obj.tipoAutobus_id

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
            try:
                numero = request.POST.get('numero', '').strip()
                matricula = request.POST.get('matricula', '').strip().upper()
                tipo_codigo = request.POST.get('tipoAutobus', '')
                marca_clave = request.POST.get('marca', '')
                modelo_clave = request.POST.get('modelo', '')

                # Validaciones
                if not numero:
                    error = 'El número del autobús es obligatorio.'
                elif not matricula:
                    error = 'La matrícula es obligatoria.'
                elif len(matricula) != 6:
                    error = 'La matrícula debe tener exactamente 6 caracteres.'
                elif not tipo_codigo:
                    error = 'El tipo de servicio es obligatorio.'
                elif not marca_clave:
                    error = 'La marca es obligatoria.'
                elif not modelo_clave:
                    error = 'El modelo es obligatorio.'
                elif Autobus.objects.filter(numero=int(numero)).exists():
                    error = f'Ya existe un autobús con el número {numero}.'
                elif Autobus.objects.filter(matricula=matricula).exists():
                    error = f'La matrícula {matricula} ya está registrada.'
                else:
                    asientos_por_tipo = {'PLUS': 44, 'PLAT': 36}
                    cant_asientos = asientos_por_tipo.get(tipo_codigo, 0)

                    wifi = request.POST.get('claveWIFI', '').strip()
                    clave_wifi = wifi.upper() if wifi else None

                    autobus = Autobus.objects.create(
                        numero=int(numero),
                        matricula=matricula,
                        claveWIFI=clave_wifi,
                        cantAsientos=cant_asientos,
                        tipoAutobus=TipoAutobus.objects.get(codigo=tipo_codigo),
                        estado=EdoAutobus.objects.get(codigo='ACTI'),
                        marca=Marca.objects.get(clave=marca_clave),
                        modelo=Modelo.objects.get(clave=modelo_clave),
                    )
                    generar_asientos(autobus)

                    request.session['toast_exito'] = f'Autobús {numero} registrado correctamente.'
                    return redirect('autobuses')

            except IntegrityError:
                error = 'Error de base de datos: verifica que los datos no estén duplicados.'
            except Exception as e:
                error = f'Error inesperado: {str(e)}'

        elif request.POST['action'] == 'baja_autobus':
            pass

 
    toast_exito = request.session.pop('toast_exito', None)

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
        'toast_exito': toast_exito,
    }
    return render(request, 'autobuses.html', context)
