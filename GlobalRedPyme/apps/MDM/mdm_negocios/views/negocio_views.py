from ..models import Negocios
from ...mdm_facturas.models import FacturasEncabezados
from ..serializers import NegociosSerializer, NegociosListarSerializer, NegociosImagenSerializer, \
    NegocioPrediccionSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
# logs
from ....CENTRAL.central_logs.methods import createLog, datosTipoLog, datosNegocios

# declaracion variables log
datosAux = datosNegocios()
datosTipoLogAux = datosTipoLog()
# asignacion datos modulo
logModulo = datosAux['modulo']
logApi = datosAux['api']
# asignacion tipo de datos
logTransaccion = datosTipoLogAux['transaccion']
logExcepcion = datosTipoLogAux['excepcion']


# CRUD NEGOCIOS
# LISTAR TODOS
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def negocio_list(request):
    """
    Este metodo sirve para listar negocios de la tabla negocios de la base datos mdm
    @type request: El campo request nombreComercial, razonSocial, ruc, empresa_id, page, page_size
    @rtype: DEvuelve una lista de negocios, caso contrario devuelve el error generado
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
            if 'nombreComercial' in request.data:
                if request.data['nombreComercial'] != '':
                    filters['nombreComercial__icontains'] = str(request.data['nombreComercial'])
            if 'razonSocial' in request.data:
                if request.data['razonSocial'] != '':
                    filters['razonSocial__icontains'] = str(request.data['razonSocial'])
            if 'ruc' in request.data:
                if request.data['ruc'] != '':
                    filters['ruc'] = str(request.data['ruc'])
            if 'empresa_id' in request.data:
                if request.data['empresa_id'] != '':
                    filters['empresa_id'] = request.data['empresa_id']
            # if 'desde' in request.data:
            #     if request.data['desde']!='':
            #         filters['created_at__startswith'] = str(request.data['desde'])
            # if 'hasta' in request.data:
            #     if request.data['hasta']!='':
            #         filters['created_at__startswith'] = str(request.data['hasta'])
            # if 'hasta' in request.data:
            #     if request.data['hasta']!='':
            #         filters['created_at__range'] = [request.data['desde'],request.data['hasta']]

            # Serializar los datos
            query = Negocios.objects.filter(**filters).order_by('-created_at')
            serializer = NegociosListarSerializer(query[offset:limit], many=True)
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
def negocio_findOne(request, pk):
    """
    Este metodo sirve para obtener un negocio de la tabla negocios de la base datos mdm
    @type pk: El campo pk recibe el id del negocio
    @type request: El campo request no recibe nada
    @rtype: DEvuelve el registro obtenido, caso contrario devuelve el error generado
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
            query = Negocios.objects.get(pk=pk, state=1)
        except Negocios.DoesNotExist:
            err = {"error": "No existe"}
            createLog(logModel, err, logExcepcion)
            return Response(err, status=status.HTTP_404_NOT_FOUND)
        # tomar el dato
        if request.method == 'GET':
            serializer = NegociosSerializer(query)
            createLog(logModel, serializer.data, logTransaccion)
            return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        err = {"error": 'Un error ha ocurrido: {}'.format(e)}
        createLog(logModel, err, logExcepcion)
        return Response(err, status=status.HTTP_400_BAD_REQUEST)


# ENCONTRAR UNO
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def negocio_findOne_ruc(request):
    """
    Este metodo sirve para obtener un negocio en la tabla negocios de la base datos mdm
    @type request: El campo request recibe el campo ruc
    @rtype: DEvuelve el registro obtenido, caso contrario devuelve el error generado
    """
    timezone_now = timezone.localtime(timezone.now())
    logModel = {
        'endPoint': logApi + 'listOne/ruc/',
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
            query = Negocios.objects.get(ruc=str(request.data['ruc']), state=1)
        except Negocios.DoesNotExist:
            err = {"error": "No existe"}
            createLog(logModel, err, logExcepcion)
            return Response(err, status=status.HTTP_404_NOT_FOUND)
        # tomar el dato
        if request.method == 'POST':
            serializer = NegociosSerializer(query)
            createLog(logModel, serializer.data, logTransaccion)
            return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        err = {"error": 'Un error ha ocurrido: {}'.format(e)}
        createLog(logModel, err, logExcepcion)
        return Response(err, status=status.HTTP_400_BAD_REQUEST)


# ENCONTRAR UNO
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def negocio_findOne_telefonoOficina(request):
    """
    Este metodo sirve para obtener el negocio de la tabla negocios de la base datos mdm
    @type request: El campo request recibe el campo telefonoOficina
    @rtype: Devuelve el registro obtenido, caso contrario devuelve el error generado
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
            query = Negocios.objects.get(telefonoOficina=str(request.data['telefonoOficina']), state=1)
        except Negocios.DoesNotExist:
            err = {"error": "No existe"}
            createLog(logModel, err, logExcepcion)
            return Response(err, status=status.HTTP_404_NOT_FOUND)
        # tomar el dato
        if request.method == 'POST':
            serializer = NegociosSerializer(query)
            createLog(logModel, serializer.data, logTransaccion)
            return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        err = {"error": 'Un error ha ocurrido: {}'.format(e)}
        createLog(logModel, err, logExcepcion)
        return Response(err, status=status.HTTP_400_BAD_REQUEST)


# CREAR
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def negocio_create(request):
    """
    Este metodo sirve para crear un negocio en la tabla negocio de la base datos mdm
    @type request: El campo request recibe los campos de la tabla negocios
    @rtype: Devuelve el registro creado, caso contrario devuelve el error generado
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

            serializer = NegociosSerializer(data=request.data)
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


# ACTUALIZAR
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def negocio_update(request, pk):
    """
    Este metodo sirve para actualizar un negocio en la tabla negocio de la base datos mdm
    @type pk: El campo request recibe el id del negocio
    @type request: El campo request recibe los campos de la tabla negocios
    @rtype: Devuelve el registro actualizar, caso contrario devuelve el error generado
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
            query = Negocios.objects.get(pk=pk, state=1)
        except Negocios.DoesNotExist:
            errorNoExiste = {'error': 'No existe'}
            createLog(logModel, errorNoExiste, logExcepcion)
            return Response(status=status.HTTP_404_NOT_FOUND)
        if request.method == 'POST':
            now = timezone.localtime(timezone.now())
            request.data['updated_at'] = str(now)
            if 'created_at' in request.data:
                request.data.pop('created_at')
            serializer = NegociosSerializer(query, data=request.data, partial=True)
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
def negocio_delete(request, pk):
    """
    ESte metodo sirve para eliminar un negocio de la tabla negocios de la base datos mdm
    @type pk: El campo pk recibe el id del negocio
    @type request: El campo request no recibe nada
    @rtype: DEvuelve el registro eliminado, caso contrario devuelve el error generado
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
            query = Negocios.objects.get(pk=pk, state=1)
        except Negocios.DoesNotExist:
            err = {"error": "No existe"}
            createLog(logModel, err, logExcepcion)
            return Response(err, status=status.HTTP_404_NOT_FOUND)
        # tomar el dato
        if request.method == 'DELETE':
            serializer = NegociosSerializer(query, data={'state': '0', 'updated_at': str(nowDate)}, partial=True)
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

    # SUBIR IMAGEN


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def negociosImagen_update(request, pk):
    """
    Este metodo sirve para actualizar la imagen del negocio de la tabla negocio de la base datos mdm
    @type pk: El campo pk recibe el id del negocio
    @type request: El campo request recibe el archivo
    @rtype: Devuelve el registro actualizado, caso contrario devuelve el error generado
    """
    timezone_now = timezone.localtime(timezone.now())
    logModel = {
        'endPoint': logApi + 'update/imagen/',
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
            query = Negocios.objects.get(pk=pk, state=1)
        except Negocios.DoesNotExist:
            errorNoExiste = {'error': 'No existe'}
            createLog(logModel, errorNoExiste, logExcepcion)
            return Response(status=status.HTTP_404_NOT_FOUND)
        if request.method == 'POST':
            now = timezone.localtime(timezone.now())
            request.data['updated_at'] = str(now)
            if 'created_at' in request.data:
                request.data.pop('created_at')
            serializer = NegociosImagenSerializer(query, data=request.data, partial=True)
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


# ENCONTRAR NEGOCIO POR FACTURA
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def negocio_by_factura_findOne(request, pk):
    """
    Este metodo sirve para buscar una factura de un negocio de la tabla factura de la base datos mdm
    @type pk: el campo pk recibe el id de la factura
    @type request: El campo request no recibe nada
    @rtype: Devuelve el registro obtenido
    """
    timezone_now = timezone.localtime(timezone.now())
    logModel = {
        'endPoint': logApi + 'cliente/factura/',
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
            query = FacturasEncabezados.objects.get(pk=pk, state=1)
        except FacturasEncabezados.DoesNotExist:
            err = {"error": "No existe"}
            createLog(logModel, err, logExcepcion)
            return Response(err, status=status.HTTP_404_NOT_FOUND)
        # tomar el dato
        if request.method == 'GET':
            serializer = NegocioPrediccionSerializer(query.negocio)
            createLog(logModel, serializer.data, logTransaccion)
            return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        err = {"error": 'Un error ha ocurrido: {}'.format(e)}
        createLog(logModel, err, logExcepcion)
        return Response(err, status=status.HTTP_400_BAD_REQUEST)


# ENCONTRAR UNO
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def negocio_prediccionRefil_findOne(request, pk):
    """
    Este metodo sirve para la prediccion de refil de la tabla negocios de la base datos mdm
    @type pk: El campo pk recibe el id
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
            query = Negocios.objects.get(pk=pk, state=1)
        except Negocios.DoesNotExist:
            err = {"error": "No existe"}
            createLog(logModel, err, logExcepcion)
            return Response(err, status=status.HTTP_404_NOT_FOUND)
        # tomar el dato
        if request.method == 'GET':
            serializer = NegocioPrediccionSerializer(query)
            createLog(logModel, serializer.data, logTransaccion)
            return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        err = {"error": 'Un error ha ocurrido: {}'.format(e)}
        createLog(logModel, err, logExcepcion)
        return Response(err, status=status.HTTP_400_BAD_REQUEST)
