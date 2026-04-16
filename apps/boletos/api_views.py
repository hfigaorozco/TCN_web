from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from datetime import date
from .models import Boleto
from apps.corridas.models import Corrida, CorridaAsiento
from apps.reservaciones.models import Reservacion, AsientoReservacion
from apps.autobuses.models import Asiento
from apps.pasajeros.models import Pasajero, TipoPasajero
from apps.login.models import Usuario


@api_view(['POST'])
def generar_boletos_api(request):
    data           = request.data
    corrida_id     = data.get('corrida_id')
    pasajeros_data = data.get('pasajeros', [])
    usuario_id     = data.get('usuario_id')  
    print(f">>> usuario_id recibido: {usuario_id}")

    if not corrida_id or not pasajeros_data:
        return Response(
            {'error': 'Faltan datos: corrida_id y pasajeros son requeridos'},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        corrida = Corrida.objects.select_related('autobus__tipoAutobus').get(numero=corrida_id)
    except Corrida.DoesNotExist:
        return Response({'error': 'Corrida no encontrada'}, status=status.HTTP_404_NOT_FOUND)

    usuario_obj = None
    if usuario_id:
        try:
            usuario_obj = Usuario.objects.get(pk=usuario_id)
        except Usuario.DoesNotExist:
            pass  

    IVA_RATE = 0.16
    subtotal = 0.0

    for p in pasajeros_data:
        try:
            tipo = TipoPasajero.objects.get(codigo=p['tipoPasajero'])
        except TipoPasajero.DoesNotExist:
            return Response(
                {'error': f"Tipo de pasajero inválido: {p['tipoPasajero']}"},
                status=status.HTTP_400_BAD_REQUEST
            )
        descuento  = corrida.tarifaBase * (tipo.porcentaje_desc / 100)
        p['precio'] = round(corrida.tarifaBase - descuento, 2)
        subtotal   += p['precio']

    iva   = round(subtotal * IVA_RATE, 2)
    total = round(subtotal + iva, 2)
    hoy   = date.today()

    pasajeros_objs = []
    for p in pasajeros_data:
        pasajero_obj = Pasajero.objects.create(
            nombre   = p['nombre'],
            apellPat = p['apellPat'],
            apellMat = p.get('apellMat', ''),
            edad     = int(p['edad']),
        )
        pasajeros_objs.append(pasajero_obj)

    reservacion = Reservacion.objects.create(
        fecha         = hoy,
        fechaLimPago  = corrida.fecha_salida,
        cantPasajeros = len(pasajeros_data),
        subtotal      = subtotal,
        IVA           = iva,
        total         = total,
        pasajero      = pasajeros_objs[0],
        corrida       = corrida,
        usuario       = usuario_obj,  
    )

    for p, pasajero_obj in zip(pasajeros_data, pasajeros_objs):
        try:
            asiento_obj = Asiento.objects.get(clave=p['asiento'], autobus=corrida.autobus)
        except Asiento.DoesNotExist:
            return Response(
                {'error': f"Asiento {p['asiento']} no encontrado"},
                status=status.HTTP_400_BAD_REQUEST
            )

        tipo_obj = TipoPasajero.objects.get(codigo=p['tipoPasajero'])

        AsientoReservacion.objects.create(asiento=asiento_obj, reservacion=reservacion)

        Boleto.objects.create(
            precio       = p['precio'],
            asiento      = asiento_obj,
            pasajero     = pasajero_obj,
            tipoPasajero = tipo_obj,
            corrida      = corrida,
        )

        CorridaAsiento.objects.filter(
            corrida=corrida, asiento=asiento_obj
        ).update(estado=CorridaAsiento.OCUPADO)

    corrida.lugaresDisp -= len(pasajeros_data)
    corrida.save()

    return Response(
        {'mensaje': 'Boletos generados correctamente', 'reservacion': reservacion.numero},
        status=status.HTTP_201_CREATED
    )