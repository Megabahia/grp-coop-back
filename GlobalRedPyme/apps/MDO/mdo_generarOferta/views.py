from .models import Oferta, OfertaDetalles
from ...GDO.gdo_gestionOferta.serializers import GestionOfertaCreateSerializer
from ...GDO.gdo_gestionOferta.models import Oferta as GDO_Oferta
from .serializers import OfertasSerializer, OfertaSerializer, OfertasListarTablaSerializer, DetallesImagenesSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from datetime import datetime
from django.core import serializers
# excel
import openpyxl
# logs
from ...CENTRAL.central_logs.methods import createLog, datosTipoLog, datosFacturas

# declaracion variables log
datosAux = datosFacturas()
datosTipoLogAux = datosTipoLog()
# asignacion datos modulo
logModulo = datosAux['modulo']
logApi = datosAux['api']
# asignacion tipo de datos
logTransaccion = datosTipoLogAux['transaccion']
logExcepcion = datosTipoLogAux['excepcion']


# CRUD PROSPECTO CLIENTES
# LISTAR TODOS
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def generarOferta_list(request):
    """
    Este metodo sirve para listar las ofertas de la tabla ofertas de la base datos mdo
    @type request: El campo request recibe negocio, cliente, empresa_id, page, page_size
    @rtype: Devuelve una lista de las ofertas, caso contrario devuelve el error generado
    """
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
            if 'negocio' in request.data:
                if request.data['negocio'] != '':
                    filters['negocio__isnull'] = False
            if 'cliente' in request.data:
                if request.data['cliente'] != '':
                    filters['cliente__isnull'] = False
            if 'empresa_id' in request.data:
                if request.data['empresa_id'] != '':
                    filters['empresa_id'] = request.data['empresa_id']
            # if 'cedula' in request.data:
            #     if request.data['cedula']!='':
            #         filters['cedula'] = str(request.data['cedula'])
            # if 'inicio' and 'fin' in request.data:                
            #     # if request.data['inicio'] !='':
            #     #     filters['created_at__startswith'] = str(request.data['inicio'])
            #     if request.data['inicio'] and request.data['fin'] !='':
            #         filters['created_at__range'] = [str(request.data['inicio']),str(request.data['fin'])]            

            # Serializar los datos
            query = Oferta.objects.filter(**filters).order_by('-created_at')
            serializer = OfertasListarTablaSerializer(query[offset:limit], many=True)
            new_serializer_data = {'cont': query.count(),
                                   'info': serializer.data}
            # envio de datos
            return Response(new_serializer_data, status=status.HTTP_200_OK)
        except Exception as e:
            err = {"error": 'Un error ha ocurrido: {}'.format(e)}
            createLog(logModel, err, logExcepcion)
            return Response(err, status=status.HTTP_400_BAD_REQUEST)

        # ENCONTRAR UNO


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def generarOferta_findOne(request, pk):
    """
    Este metodo sirve para obtener una oferta de la tabla oferta de la base datos
    @type pk: El campo pk recibe el campo id de la oferta
    @type request: El campo request no recibe nada
    @rtype: Devuelve el registro encontrado, caso contrario devuelve el error generado
    """
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
            query = Oferta.objects.get(pk=pk, state=1)
        except Oferta.DoesNotExist:
            err = {"error": "No existe"}
            createLog(logModel, err, logExcepcion)
            return Response(err, status=status.HTTP_404_NOT_FOUND)
        # tomar el dato
        if request.method == 'GET':
            serializer = OfertasSerializer(query)
            createLog(logModel, serializer.data, logTransaccion)
            return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        err = {"error": 'Un error ha ocurrido: {}'.format(e)}
        createLog(logModel, err, logExcepcion)
        return Response(err, status=status.HTTP_400_BAD_REQUEST)


# CREAR
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def generarOferta_create(request):
    """
    Este metodo sirve para crear una oferta en la tabla oferta de la base datos mdo
    @type request: El campo request recibe los campos de la tabla oferta
    @rtype: DEvuelve el registro creado, caso contrario devuelve el error generado
    """
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
            logModel['dataEnviada'] = str(request.data)
            request.data['created_at'] = str(timezone_now)
            if 'updated_at' in request.data:
                request.data.pop('updated_at')

            serializer = OfertaSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                request.data['fechaOferta'] = request.data['fecha']
                request.data['codigo'] = serializer.data['id']
                gestionOfertaSerializer = GestionOfertaCreateSerializer(data=request.data)
                if gestionOfertaSerializer.is_valid():
                    gestionOfertaSerializer.save()
                    createLog(logModel, serializer.data, logTransaccion)
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                createLog(logModel, gestionOfertaSerializer.errors, logExcepcion)
                return Response(gestionOfertaSerializer.errors, status=status.HTTP_400_BAD_REQUEST)
            createLog(logModel, serializer.errors, logExcepcion)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            err = {"error": 'Un error ha ocurrido: {}'.format(e)}
            createLog(logModel, err, logExcepcion)
            return Response(err, status=status.HTTP_400_BAD_REQUEST)


# ACTUALIZAR
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def generarOferta_update(request, pk):
    """
    Este metodo sirve para actualizar una oferta en la tabla oferta de la base datos mdo
    @type pk: El campo pk recibe el id de la oferta
    @type request: El campo request recibe los campos de la tabla oferta
    @rtype: DEvuelve el registro actualizada, caso contrario devuelve el error generado
    """
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
            query = Oferta.objects.get(pk=pk, state=1)
        except Oferta.DoesNotExist:
            errorNoExiste = {'error': 'No existe'}
            createLog(logModel, errorNoExiste, logExcepcion)
            return Response(status=status.HTTP_404_NOT_FOUND)
        if request.method == 'POST':
            now = timezone.localtime(timezone.now())
            request.data['updated_at'] = str(now)
            if 'created_at' in request.data:
                request.data.pop('created_at')
            serializer = OfertasSerializer(query, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
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
def generarOferta_delete(request, pk):
    """
    Este metodo sirve para borrar la oferta de la tabla oferta de la base datos mdo
    @type pk: EL campo pk recibe el id de la oferta
    @type request: El campo request no recibe nada
    @rtype: DEvuelve el registro borrado, caso contrario devuelve el error generado
    """
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
            query = Oferta.objects.get(pk=pk, state=1)
        except Oferta.DoesNotExist:
            err = {"error": "No existe"}
            createLog(logModel, err, logExcepcion)
            return Response(err, status=status.HTTP_404_NOT_FOUND)
            return Response(status=status.HTTP_404_NOT_FOUND)
        # tomar el dato
        if request.method == 'DELETE':
            serializer = OfertaSerializer(query, data={'state': '0', 'updated_at': str(nowDate)}, partial=True)
            if serializer.is_valid():
                GDO_Oferta.objects.filter(codigo=query.id, state=1).update(state=0, updated_at=str(nowDate))
                serializer.save()
                createLog(logModel, serializer.data, logTransaccion)
                return Response(serializer.data, status=status.HTTP_200_OK)
            createLog(logModel, serializer.errors, logExcepcion)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        err = {"error": 'Un error ha ocurrido: {}'.format(e)}
        createLog(logModel, err, logExcepcion)
        return Response(err, status=status.HTTP_400_BAD_REQUEST)

    # ENCONTRAR DETALLES DE OFERTA GENERADA


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def detalles_list(request, pk):
    """
    Este mwtodo sirve para listar los detalles de la oferta de la tabla detalles oferta de la base datos mdo
    @type pk: el campo pk recibe el id la oferta
    @type request: El campo request no recibe nada
    @rtype: Devuelve una lista de los detalles, caso contrario devuelve el error generado
    """
    timezone_now = timezone.localtime(timezone.now())
    logModel = {
        'endPoint': logApi + 'productosImagenes/',
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
            query = OfertaDetalles.objects.filter(oferta=pk, state=1)
        except OfertaDetalles.DoesNotExist:
            err = {"error": "No existe"}
            createLog(logModel, err, logExcepcion)
            return Response(err, status=status.HTTP_404_NOT_FOUND)
        # tomar el dato
        if request.method == 'GET':
            serializer = DetallesImagenesSerializer(query, many=True)
            createLog(logModel, serializer.data, logTransaccion)
            return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        err = {"error": 'Un error ha ocurrido: {}'.format(e)}
        createLog(logModel, err, logExcepcion)
        return Response(err, status=status.HTTP_400_BAD_REQUEST)
