from django.shortcuts import render, redirect
from .models import Autobus, Marca, Modelo, TipoAutobus, EdoAutobus

def pagina_autobuses(request):

    if request.method == 'POST' and 'action' in request.POST:

        if request.POST['action'] == 'agregar_autobus':
            tipo_codigo = request.POST['tipoAutobus']

            asientos_por_tipo = {
                'PLUS': 44,
                'PLAT': 36,
            }
            cant_asientos = asientos_por_tipo.get(tipo_codigo, 0)

            Autobus.objects.create(
                numero=request.POST['numero'],
                matricula=request.POST['matricula'],
                claveWIFI=request.POST.get('claveWIFI') or None,
                cantAsientos=cant_asientos,
                tipoAutobus=TipoAutobus.objects.get(codigo=tipo_codigo),
                estado=EdoAutobus.objects.get(codigo='ACTI'),
                marca=Marca.objects.get(clave=request.POST['marca']),
                modelo=Modelo.objects.get(clave=request.POST['modelo']),
            )
            return redirect('autobuses')

        elif request.POST['action'] == 'baja_autobus':
            autobus = Autobus.objects.get(numero=request.POST['numero'])
            autobus.estado = EdoAutobus.objects.get(codigo='INAC')
            autobus.save()
            return redirect('autobuses')

        elif request.POST['action'] == 'agregar_marca':
            Marca.objects.create(
                clave=request.POST['clave'],
                nombre=request.POST['nombre'],
            )
            return redirect('autobuses')

        elif request.POST['action'] == 'agregar_modelo':
            Modelo.objects.create(
                clave=request.POST['clave'],
                nombre=request.POST['nombre'],
                marca=Marca.objects.get(clave=request.POST['marca']),
            )
            return redirect('autobuses')

    autobuses = Autobus.objects.filter(estado__codigo='ACTI')

    context = {
        'autobuses': autobuses,
        'marcas': Marca.objects.all(),
        'modelos': Modelo.objects.all(),
        'tipos_autobus': TipoAutobus.objects.all(),
        'total_activos': autobuses.count(),
        'total_disponibles': autobuses.filter(estado__descripcion='Disponible').count(),
        'total_en_ruta': autobuses.filter(estado__descripcion='En Ruta').count(),
    }

    return render(request, 'autobuses.html', context)