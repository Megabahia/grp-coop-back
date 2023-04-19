from .models import MovimientoCobros
from ...CORP.corp_autorizaciones.models import Autorizaciones
from ...CORE.core_monedas.models import Monedas
from ...CORP.corp_pagos.models import Pagos
from ...CORP.corp_monedasEmpresa.models import MonedasEmpresa
from .serializers import (
    MovimientoCobrosSerializer
)
from .producer import publish_monedas
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
# Swagger
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
# ObjectId
from bson import ObjectId
# logs
from ...CENTRAL.central_logs.methods import createLog, datosTipoLog, datosProductosMDP

# declaracion variables log
datosAux = datosProductosMDP()
datosTipoLogAux = datosTipoLog()
# asignacion datos modulo
logModulo = datosAux['modulo']
logApi = datosAux['api']
# asignacion tipo de datos
logTransaccion = datosTipoLogAux['transaccion']
logExcepcion = datosTipoLogAux['excepcion']


# CRUD CORP
# LISTAR TODOS
# 'methods' can be used to apply the same modification to multiple methods
@swagger_auto_schema(methods=['post'],
                     request_body=openapi.Schema(
                         type=openapi.TYPE_OBJECT,
                         required=['page_size', 'page'],
                         properties={
                             'page_size': openapi.Schema(type=openapi.TYPE_NUMBER),
                             'page': openapi.Schema(type=openapi.TYPE_NUMBER),
                             'identificacion': openapi.Schema(type=openapi.TYPE_STRING),
                             'codigoCobro': openapi.Schema(type=openapi.TYPE_STRING),
                             'monto': openapi.Schema(type=openapi.TYPE_STRING),
                             'correo': openapi.Schema(type=openapi.TYPE_STRING),
                         },
                     ),
                     operation_description='Uninstall a version of Site',
                     responses={200: MovimientoCobrosSerializer(many=True)})
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def movimientoCobros_list(request):
    timezone_now = timezone.localtime(timezone.now())
    logModel = {
        'endPoint': logApi + 'list/',
        'modulo': logModulo,
        'tipo': logExcepcion,
        'accion': 'LEER',
        'fechaInicio': str(timezone_now),
        'dataEnviada': '{}',
        'fechaFin': str(timezone_now),
        'dataRecibida': '{}'
    }
    if request.method == 'POST':
        try:
            logModel['dataEnviada'] = str(request.data)
            # paginacion
            page_size = int(request.data['page_size'])
            page = int(request.data['page'])
            offset = page_size * page
            limit = offset + page_size
            # Filtros
            filters = {"state": "1"}

            if 'identificacion' in request.data:
                if request.data['identificacion'] != '':
                    filters['identificacion__icontains'] = str(request.data['identificacion'])
            if 'codigoCobro' in request.data:
                if request.data['codigoCobro'] != '':
                    filters['codigoCobro__icontains'] = str(request.data['codigoCobro'])
            if 'monto' in request.data:
                if request.data['monto'] != '':
                    filters['monto__icontains'] = str(request.data['monto'])
            if 'correo' in request.data:
                if request.data['correo'] != '':
                    filters['correo__icontains'] = str(request.data['correo'])

            # Serializar los datos
            query = MovimientoCobros.objects.filter(**filters).order_by('estado')
            serializer = MovimientoCobrosSerializer(query[offset:limit], many=True)
            new_serializer_data = {'cont': query.count(),
                                   'info': serializer.data}
            # envio de datos
            return Response(new_serializer_data, status=status.HTTP_200_OK)
        except Exception as e:
            err = {"error": 'Un error ha ocurrido: {}'.format(e)}
            createLog(logModel, err, logExcepcion)
            return Response(err, status=status.HTTP_400_BAD_REQUEST)


# CREAR
# 'methods' can be used to apply the same modification to multiple methods
@swagger_auto_schema(methods=['post'], request_body=MovimientoCobrosSerializer)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def movimientoCobros_create(request):
    timezone_now = timezone.localtime(timezone.now())
    logModel = {
        'endPoint': logApi + 'create/',
        'modulo': logModulo,
        'tipo': logExcepcion,
        'accion': 'CREAR',
        'fechaInicio': str(timezone_now),
        'dataEnviada': '{}',
        'fechaFin': str(timezone_now),
        'dataRecibida': '{}'
    }
    if request.method == 'POST':
        try:
            monedasUsuario = Monedas.objects.filter(user_id=request.data['user_id'], state=1).order_by(
                '-created_at').first()
            if float(monedasUsuario.saldo) < float(request.data['montoSupermonedas']):
                data = {'error': 'Supera las monedas de su cuenta.'}
                return Response(data, status=status.HTTP_400_BAD_REQUEST)

            logModel['dataEnviada'] = str(request.data)
            request.data['created_at'] = str(timezone_now)
            if 'updated_at' in request.data:
                request.data.pop('updated_at')

            serializer = MovimientoCobrosSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                Pagos.objects.filter(codigoCobro=request.data['codigoCobro']).update(state=0)
                request.data['nombreCompleto'] = request.data['nombres'] + ' ' + request.data['apellidos']
                datos = {
                    'numeroFactura': request.data['numeroFactura'],
                    'montoSupermonedas': request.data['montoSupermonedas'],
                    'montoTotalFactura': request.data['montoTotalFactura'],
                    'nombreCompleto': request.data['nombreCompleto'],
                    'nombres': request.data['nombres'],
                    'apellidos': request.data['apellidos'],
                    'identificacion': request.data['identificacion'],
                    'whatsapp': request.data['whatsapp'],
                    'empresa_id': request.data['empresa_id']
                }
                MonedasEmpresa.objects.create(**datos)
                monedasEmpresa = Monedas.objects.filter(empresa_id=str(request.data['empresa_id']), user_id=None,
                                                        autorizador_id=None).order_by('-created_at').first()
                dataEmpresa = {
                    'empresa_id': str(request.data['empresa_id']),
                    'tipo': 'Credito',
                    'estado': 'aprobado',
                    'credito': float(request.data['montoSupermonedas']),
                    'saldo': float(
                        request.data['montoSupermonedas']) if monedasEmpresa is None else monedasEmpresa.saldo + float(
                        request.data['montoSupermonedas']),
                    'descripcion': 'Cobro de monedas generado por comprobante de compra.'
                }
                Monedas.objects.create(**dataEmpresa)
                # saldo = monedasUsuario.saldo - float(request.data['montoSupermonedas'])
                publish_monedas({
                    'user_id': request.data['user_id'],
                    'empresa_id': request.data['empresa_id'],
                    'tipo': 'Debito',
                    'debito': request.data['montoSupermonedas']
                })
                # Monedas.objects.create(user_id=request.data['user_id'],empresa_id=request.data['empresa_id'],tipo='Debito',debito=request.data['montoSupermonedas'],saldo=saldo)
                createLog(logModel, serializer.data, logTransaccion)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            createLog(logModel, serializer.errors, logExcepcion)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            err = {"error": 'Un error ha ocurrido: {}'.format(e)}
            createLog(logModel, err, logExcepcion)
            return Response(err, status=status.HTTP_400_BAD_REQUEST)


# ENCONTRAR UNO
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def movimientoCobros_listOne(request, pk):
    timezone_now = timezone.localtime(timezone.now())
    logModel = {
        'endPoint': logApi + 'listOne/',
        'modulo': logModulo,
        'tipo': logExcepcion,
        'accion': 'LEER',
        'fechaInicio': str(timezone_now),
        'dataEnviada': '{}',
        'fechaFin': str(timezone_now),
        'dataRecibida': '{}'
    }
    try:
        try:
            # Creo un ObjectoId porque la primaryKey de mongo es ObjectId
            pk = ObjectId(pk)
            query = MovimientoCobros.objects.get(pk=pk, state=1)
        except MovimientoCobros.DoesNotExist:
            err = {"error": "No existe"}
            createLog(logModel, err, logExcepcion)
            return Response(err, status=status.HTTP_404_NOT_FOUND)
        # tomar el dato
        if request.method == 'GET':
            serializer = MovimientoCobrosSerializer(query)
            createLog(logModel, serializer.data, logTransaccion)
            return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        err = {"error": 'Un error ha ocurrido: {}'.format(e)}
        createLog(logModel, err, logExcepcion)
        return Response(err, status=status.HTTP_400_BAD_REQUEST)


# ACTUALIZAR
# 'methods' can be used to apply the same modification to multiple methods
@swagger_auto_schema(methods=['post'], request_body=MovimientoCobrosSerializer)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def movimientoCobros_update(request, pk):
    timezone_now = timezone.localtime(timezone.now())
    logModel = {
        'endPoint': logApi + 'update/',
        'modulo': logModulo,
        'tipo': logExcepcion,
        'accion': 'ESCRIBIR',
        'fechaInicio': str(timezone_now),
        'dataEnviada': '{}',
        'fechaFin': str(timezone_now),
        'dataRecibida': '{}'
    }
    try:
        try:
            logModel['dataEnviada'] = str(request.data)
            # Creo un ObjectoId porque la primaryKey de mongo es ObjectId
            pk = ObjectId(pk)
            query = MovimientoCobros.objects.get(pk=pk, state=1)
        except MovimientoCobros.DoesNotExist:
            errorNoExiste = {'error': 'No existe'}
            createLog(logModel, errorNoExiste, logExcepcion)
            return Response(status=status.HTTP_404_NOT_FOUND)
        if request.method == 'POST':
            now = timezone.localtime(timezone.now())
            request.data['updated_at'] = str(now)
            if 'created_at' in request.data:
                request.data.pop('created_at')

            serializer = MovimientoCobrosSerializer(query, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                if request.data['estado'] == 'Pre-autorizado':
                    autorizacion = Autorizaciones.objects.filter(cobrar=query).first()
                    if autorizacion is None:
                        Autorizaciones.objects.create(codigoAutorizacion='', estado=request.data['estado'],
                                                      user_id=request.data['user_id'], cobrar=query)
                    else:
                        autorizacion.estado = request.data['estado']
                        autorizacion.save()
                createLog(logModel, serializer.data, logTransaccion)
                return Response(serializer.data)
            createLog(logModel, serializer.errors, logExcepcion)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        err = {"error": 'Un error ha ocurrido: {}'.format(e)}
        createLog(logModel, err, logExcepcion)
        return Response(err, status=status.HTTP_400_BAD_REQUEST)


# ELIMINAR
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def movimientoCobros_delete(request, pk):
    nowDate = timezone.localtime(timezone.now())
    logModel = {
        'endPoint': logApi + 'delete/',
        'modulo': logModulo,
        'tipo': logExcepcion,
        'accion': 'BORRAR',
        'fechaInicio': str(nowDate),
        'dataEnviada': '{}',
        'fechaFin': str(nowDate),
        'dataRecibida': '{}'
    }
    try:
        try:
            # Creo un ObjectoId porque la primaryKey de mongo es ObjectId
            pk = ObjectId(pk)
            persona = MovimientoCobros.objects.get(pk=pk, state=1)
        except MovimientoCobros.DoesNotExist:
            err = {"error": "No existe"}
            createLog(logModel, err, logExcepcion)
            return Response(err, status=status.HTTP_404_NOT_FOUND)
            return Response(status=status.HTTP_404_NOT_FOUND)
        # tomar el dato
        if request.method == 'DELETE':
            serializer = MovimientoCobrosSerializer(persona, data={'state': '0', 'updated_at': str(nowDate)},
                                                    partial=True)
            if serializer.is_valid():
                serializer.save()
                createLog(logModel, serializer.data, logTransaccion)
                return Response(serializer.data, status=status.HTTP_200_OK)
            createLog(logModel, serializer.errors, logExcepcion)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        err = {"error": 'Un error ha ocurrido: {}'.format(e)}
        createLog(logModel, err, logExcepcion)
        return Response(err, status=status.HTTP_400_BAD_REQUEST)
