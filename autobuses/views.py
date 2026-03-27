from django.shortcuts import render, redirect
from .models import Autobus, Marca, Modelo, TipoAutobus, EdoAutobus

def pagina_autobuses(request):
    error = None

    if request.method == 'POST' and 'action' in request.POST:

        if request.POST['action'] == 'agregar_autobus':
            
            tipo_codigo = request.POST['tipoAutobus']
            asientos_por_tipo = {'PLUS': 44, 'PLAT': 36}
            cant_asientos = asientos_por_tipo.get(tipo_codigo, 0)

            Autobus.objects.create(
                numero=int(request.POST['numero']),         
                matricula=request.POST['matricula'].upper(), 
                claveWIFI=request.POST.get('claveWIFI') or None,
                cantAsientos=cant_asientos,
                tipoAutobus=TipoAutobus.objects.get(codigo=tipo_codigo),
                estado=EdoAutobus.objects.get(codigo='ACTI'), 
                marca=Marca.objects.get(clave=request.POST['marca']),
                modelo=Modelo.objects.get(clave=request.POST['modelo']),
            )
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