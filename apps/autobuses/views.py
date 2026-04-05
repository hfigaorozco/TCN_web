from django.shortcuts import render, redirect
from django.db import IntegrityError, models
from django.utils import timezone
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
    error_tipo = None

    if request.method == 'POST' and 'action' in request.POST:
        action = request.POST['action']

        if action == 'agregar_autobus':
            try:
                numero       = request.POST.get('numero', '').strip()
                matricula    = request.POST.get('matricula', '').strip().upper()
                tipo_codigo  = request.POST.get('tipoAutobus', '')
                marca_clave  = request.POST.get('marca', '')
                modelo_clave = request.POST.get('modelo', '')

                if not numero:
                    error = 'El número del autobús es obligatorio'
                elif not matricula:
                    error = 'La matrícula es obligatoria'
                elif len(matricula) != 6:
                    error = 'La matrícula debe tener exactamente 6 caracteres'
                elif not tipo_codigo:
                    error = 'El tipo de servicio es obligatorio'
                elif not marca_clave:
                    error = 'La marca es obligatoria'
                elif not modelo_clave:
                    error = 'El modelo es obligatorio'
                elif Autobus.objects.filter(numero=int(numero)).exists():
                    error = f'Autobús número {numero} ya existe'
                elif Autobus.objects.filter(matricula=matricula).exists():
                    error = f'La matrícula {matricula} ya está registrada'
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
                error = 'Error de base de datos: datos duplicados.'
            except Exception as e:
                error = f'Error inesperado: {str(e)}'

            error_tipo = 'agregar_autobus'

        elif action == 'baja_autobus':
            try:
                numero = request.POST.get('numero', '').strip()

                if not numero:
                    error = 'Debes seleccionar un autobús'
                else:
                    autobus = Autobus.objects.get(numero=int(numero))
                    edo_baja = EdoAutobus.objects.get(codigo='INAC')
                    autobus.estado = edo_baja
                    autobus.save()
                    request.session['toast_exito'] = f'Autobús {numero} dado de baja exitosamente'
                    return redirect('autobuses')

            except Autobus.DoesNotExist:
                error = f'No se encontró el autobús {numero}'
            except EdoAutobus.DoesNotExist:
                error = 'No existe el estado en la base de datos'
            except Exception as e:
                error = f'Error: {str(e)}'

            error_tipo = 'baja_autobus'

        elif action == 'agregar_marca':
            try:
                codigo = request.POST.get('codigo', '').strip().upper()
                nombre = request.POST.get('nombre', '').strip()

                if not codigo:
                    error = 'El código de la marca es obligatorio'
                elif not nombre:
                    error = 'El nombre de la marca es obligatorio'
                elif Marca.objects.filter(clave=codigo).exists():
                    error = f'Ya existe una marca con el código {codigo}'
                else:
                    Marca.objects.create(clave=codigo, nombre=nombre)
                    request.session['toast_exito'] = f'Marca {nombre} registrada correctamente'
                    return redirect('autobuses')

            except IntegrityError:
                error = 'Error de base de datos: código de marca duplicado.'
            except Exception as e:
                error = f'Error inesperado: {str(e)}'

            error_tipo = 'agregar_marca'

        elif action == 'agregar_modelo':
            try:
                codigo      = request.POST.get('codigo', '').strip().upper()
                nombre      = request.POST.get('nombre', '').strip()
                marca_clave = request.POST.get('marca', '')

                if not codigo:
                    error = 'El código del modelo es obligatorio.'
                elif not nombre:
                    error = 'El nombre del modelo es obligatorio.'
                elif not marca_clave:
                    error = 'La marca es obligatoria.'
                elif Modelo.objects.filter(clave=codigo).exists():
                    error = f'Ya existe un modelo con el código {codigo}.'
                else:
                    Modelo.objects.create(
                        clave=codigo,
                        nombre=nombre,
                        marca=Marca.objects.get(clave=marca_clave),
                    )
                    request.session['toast_exito'] = f'Modelo {nombre} registrado correctamente.'
                    return redirect('autobuses')

            except IntegrityError:
                error = 'Error de base de datos: código de modelo duplicado.'
            except Exception as e:
                error = f'Error inesperado: {str(e)}'

            error_tipo = 'agregar_modelo'

    # ========== CONTEXTO ==========
    toast_exito = request.session.pop('toast_exito', None)
    autobuses   = Autobus.objects.filter(estado__codigo='ACTI')

    # --- Lógica de autobuses en ruta ---
    ahora        = timezone.localtime()
    hora_actual  = ahora.time()
    fecha_actual = ahora.date()

    # Caso 1: corrida normal (no cruza medianoche)
    #   fecha_salida = hoy, hora_salida <= ahora <= hora_llegada, hora_llegada >= hora_salida
    en_ruta_normal = autobuses.filter(
        corridas__estado__codigo='ACT',
        corridas__fecha_salida=fecha_actual,
        corridas__hora_salida__lte=hora_actual,
        corridas__hora_llegada__gte=hora_actual,
    ).exclude(
        corridas__hora_llegada__lt=models.F('corridas__hora_salida')
    )

    # Caso 2: corrida que cruza medianoche — primera parte (aún es el día de salida)
    #   fecha_salida = hoy, hora_salida <= ahora, hora_llegada < hora_salida
    en_ruta_cruce_ida = autobuses.filter(
        corridas__estado__codigo='ACT',
        corridas__fecha_salida=fecha_actual,
        corridas__hora_salida__lte=hora_actual,
        corridas__hora_llegada__lt=models.F('corridas__hora_salida'),
    )

    # Caso 3: corrida que cruzó medianoche — segunda parte (ya es el día de llegada)
    #   fecha_llegada = hoy, hora_llegada >= ahora, hora_llegada < hora_salida
    en_ruta_cruce_vuelta = autobuses.filter(
        corridas__estado__codigo='ACT',
        corridas__fecha_llegada=fecha_actual,
        corridas__hora_llegada__gte=hora_actual,
        corridas__hora_llegada__lt=models.F('corridas__hora_salida'),
    )

    autobuses_en_ruta = (
        en_ruta_normal | en_ruta_cruce_ida | en_ruta_cruce_vuelta
    ).distinct()

    context = {
        'autobuses':         autobuses,
        'marcas':            Marca.objects.all(),
        'modelos':           Modelo.objects.all(),
        'tipos_autobus':     TipoAutobus.objects.all(),
        'total_activos':     autobuses.count(),
        'total_disponibles': autobuses.exclude(pk__in=autobuses_en_ruta).count(),
        'total_en_ruta':     autobuses_en_ruta.count(),
        'error':             error,
        'error_tipo':        error_tipo,
        'toast_exito':       toast_exito,
    }
    return render(request, 'autobuses.html', context)