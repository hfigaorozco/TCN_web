from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Ruta, Ciudad


def rutas_view(request):
    rutas = Ruta.objects.all()
    ciudades = Ciudad.objects.all()
    total_rutas = rutas.count()

    context = {
        'rutas': rutas,
        'ciudades': ciudades,
        'total_rutas': total_rutas,
    }

    return render(request, 'rutas.html', context)

def agregar_ciudad(request):
    if request.method == 'POST':
        try:
            codigo = request.POST['codigo']
            nombre = request.POST['nombre']

            Ciudad.objects.create(
                codigo=codigo,
                nombre=nombre
            )
            messages.success(request, f"Ciudad {nombre} agregada correctamente.")
        except Exception as e:
            messages.error(request, f"Error al agregar ciudad: {str(e)}")

    return redirect('rutas')


def editar_ciudad(request):
    if request.method == 'POST':
        try:
            original_codigo = request.POST.get('original_codigo')
            nuevo_codigo = request.POST.get('codigo')
            nuevo_nombre = request.POST.get('nombre')

            ciudad = Ciudad.objects.get(codigo=original_codigo)
            
            if original_codigo != nuevo_codigo:
                nueva_ciudad = Ciudad.objects.create(codigo=nuevo_codigo, nombre=nuevo_nombre)
                Ruta.objects.filter(ciudadOrigen=ciudad).update(ciudadOrigen=nueva_ciudad)
                Ruta.objects.filter(ciudadDestino=ciudad).update(ciudadDestino=nueva_ciudad)
                ciudad.delete()
            else:
                ciudad.nombre = nuevo_nombre
                ciudad.save()
            
            messages.success(request, f"Ciudad {nuevo_nombre} actualizada correctamente.")
        except Exception as e:
            messages.error(request, f"Error al actualizar ciudad: {str(e)}")

    return redirect('rutas')


def agregar_ruta(request):
    if request.method == 'POST':
        try:
            origen_id = request.POST['ciudadOrigen']
            destino_id = request.POST['ciudadDestino']
            distancia = request.POST['distancia']

            if origen_id == destino_id:
                messages.error(request, "El origen y destino no pueden ser la misma ciudad.")
                return redirect('rutas')

            nuevo_codigo = f"{origen_id}-{destino_id}"

            if Ruta.objects.filter(
                ciudadOrigen_id=origen_id,
                ciudadDestino_id=destino_id
            ).exists() or Ruta.objects.filter(
                ciudadOrigen_id=destino_id,
                ciudadDestino_id=origen_id
            ).exists():
                messages.error(request, "Ya existe una ruta entre estas ciudades.")
                return redirect('rutas')

            Ruta.objects.create(
                codigo=nuevo_codigo,
                ciudadOrigen_id=origen_id,
                ciudadDestino_id=destino_id,
                distancia=distancia
            )

            messages.success(request, f"Ruta {nuevo_codigo} agregada correctamente.")

        except Exception as e:
            messages.error(request, f"Error al agregar ruta: {str(e)}")

    return redirect('rutas')


def editar_ruta(request):
    if request.method == 'POST':
        try:
            codigo = request.POST['codigo']
            distancia = request.POST['distancia']

            ruta = Ruta.objects.get(codigo=codigo)
            ruta.distancia = distancia
            ruta.save()
            messages.success(request, "Ruta actualizada correctamente.")
        except Exception as e:
            messages.error(request, f"Error al actualizar ruta: {str(e)}")

    return redirect('rutas')