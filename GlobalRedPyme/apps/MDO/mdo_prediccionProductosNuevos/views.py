from django.db.models import Avg
from .models import (
    PrediccionProductosNuevos, Detalles
)
from .serializers import (
    PrediccionProductosListSerializer, PrediccionProductosSerializer, DetallesImagenesSerializer,
    PrediccionNuevosProductosSerializer
)
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
import datetime
# Request
import requests
from ...config import config
# excel
import openpyxl
# logs
from ...CENTRAL.central_logs.methods import createLog, datosTipoLog, datosPrediccionProductosNuevosMDO

# declaracion variables log
datosAux = datosPrediccionProductosNuevosMDO()
datosTipoLogAux = datosTipoLog()
# asignacion datos modulo
logModulo = datosAux['modulo']
logApi = datosAux['api']
# asignacion tipo de datos
logTransaccion = datosTipoLogAux['transaccion']
logExcepcion = datosTipoLogAux['excepcion']


# CRUD PRODUCTOS
# LISTAR TODOS
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def prediccionProductosNuevos_list(request):
    """
    Este metodo sirve para listar predicciones de la tabla predicciones de la base datos mdo
    @type request: El campo request recibe page, page_size, inicio, fin, cliente, negocio, identificacion, empresa_id
    @rtype: Devuelve una lista de las predicciones, caso contrario devuelve el error generado
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
            if request.data['inicio'] != '':
                filters['fechaPredicciones__gte'] = str(request.data['inicio'])
            if request.data['fin'] != '':
                filters['fechaPredicciones__lte'] = str(request.data['fin'])
            if 'cliente' in request.data:
                if request.data['cliente'] != '':
                    filters['cliente__isnull'] = False
            if 'negocio' in request.data:
                if request.data['negocio'] != '':
                    filters['negocio__isnull'] = False
            if 'identificacion' in request.data:
                if request.data['identificacion'] != '':
                    filters['identificacion__icontains'] = str(request.data['identificacion'])
            if 'empresa_id' in request.data:
                if request.data['empresa_id'] != '':
                    filters['empresa_id'] = request.data['empresa_id']

            # Serializar los datos
            query = PrediccionProductosNuevos.objects.filter(**filters).order_by('-created_at')
            serializer = PrediccionProductosListSerializer(query[offset:limit], many=True)
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
def detalles_list(request, pk):
    """
    Este metodo sirve para listar los detalles de la tabla detalles de la base datos mdo
    @type pk: El campo pk recibe el id de prediccion
    @type request: EL CAMPO request no recibe
    @rtype: DEvuelve una lista de los detalles, caso contrario devuelve el error generado
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
            query = Detalles.objects.filter(prediccionProductosNuevos=pk, state=1)
        except Detalles.DoesNotExist:
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


# CREAR
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def prediccionProductosNuevos_create(request):
    """
    Este metodo sirve para crear la prediccion de la tabla predicciones de la base datos mdo
    @type request: El campo request recibe los campos de la table predicciones
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

            serializer = PrediccionProductosSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                createLog(logModel, serializer.data, logTransaccion)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            createLog(logModel, serializer.errors, logExcepcion)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            err = {"error": 'Un error ha ocurrido: {}'.format(e)}
            createLog(logModel, err, logExcepcion)
            return Response(err, status=status.HTTP_400_BAD_REQUEST)


# ENCONTRAR UNA PREDICCION CROSSELING
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def prediccion_productosNuevos_listOne(request, pk):
    """
    Este metodo sirve para obtener una prediccion de la tabla predicciones de la base datos mdo
    @type pk: El campo pk recibe el id de la preccion
    @type request: El campo request no recibe nada
    @rtype: DEvuelve el registro encontrado, caso contrario devuelve el error generado
    """
    timezone_now = timezone.localtime(timezone.now())
    logModel = {
        'endPoint': logApi + 'prediccionProductosNuevos/',
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
            query = Detalles.objects.filter(prediccionProductosNuevos=pk, state=1)
        except Detalles.DoesNotExist:
            err = {"error": "No existe"}
            createLog(logModel, err, logExcepcion)
            return Response(err, status=status.HTTP_404_NOT_FOUND)
        # tomar el dato
        if request.method == 'GET':
            today = datetime.date.today()
            prediccionUltimoTotal = PrediccionProductosNuevos.objects.filter(pk=pk).aggregate(ultimoTotal=Avg('total'))
            prediccionTotalAnio = PrediccionProductosNuevos.objects.filter(created_at__year=today.year).aggregate(
                ultimoTotal=Avg('total'))
            prediccionTotalMes = PrediccionProductosNuevos.objects.filter(created_at__month=today.month).aggregate(
                ultimoTotal=Avg('total'))
            serializer = PrediccionNuevosProductosSerializer(query, many=True)
            auth_token = request.META['HTTP_AUTHORIZATION']
            hed = {'Authorization': auth_token}
            if query[0].prediccionProductosNuevos.cliente is not None:
                r = requests.get(config.API_BACK_END + 'mdm/clientes/cliente/factura/' + str(
                    query[0].prediccionProductosNuevos.factura_id), headers=hed)
                data = {'cliente': r.json(), 'productos': serializer.data
                    , 'comprasMensuales': prediccionTotalMes['ultimoTotal']
                    , 'comprasAnuales': prediccionTotalAnio['ultimoTotal']
                    , 'ultimoTotal': prediccionUltimoTotal['ultimoTotal']}
            else:
                r = requests.get(config.API_BACK_END + 'mdm/negocios/negocio/factura/' + str(
                    query[0].prediccionProductosNuevos.factura_id), headers=hed)
                data = {'negocio': r.json(), 'productos': serializer.data
                    , 'comprasMensuales': prediccionTotalMes['ultimoTotal']
                    , 'comprasAnuales': prediccionTotalAnio['ultimoTotal']
                    , 'ultimoTotal': prediccionUltimoTotal['ultimoTotal']}

            createLog(logModel, serializer.data, logTransaccion)
            return Response(data, status=status.HTTP_200_OK)
    except Exception as e:
        err = {"error": 'Un error ha ocurrido: {}'.format(e)}
        createLog(logModel, err, logExcepcion)
        return Response(err, status=status.HTTP_400_BAD_REQUEST)
