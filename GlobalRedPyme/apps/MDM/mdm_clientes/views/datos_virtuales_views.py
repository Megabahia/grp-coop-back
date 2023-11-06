from ..models import DatosVirtualesClientes
from ..serializers import DatosVirtualesClientesSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
# logs
from ....CENTRAL.central_logs.methods import createLog, datosTipoLog, datosClientes

# declaracion variables log
datosAux = datosClientes()
datosTipoLogAux = datosTipoLog()
# asignacion datos modulo
logModulo = datosAux['modulo']
logApi = datosAux['api']
# asignacion tipo de datos
logTransaccion = datosTipoLogAux['transaccion']
logExcepcion = datosTipoLogAux['excepcion']


# CRUD PERSONAL NEGOCIOS
# LISTAR TODOS
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def datosVirtuales_list(request, pk):
    """
    Este metodo sirve para listar los datos virtuales de la tabla virtuales de la base datos mdm
    @type pk: El campo pk recibe el id del cliente
    @type request: El campo request recibe page, page_size
    @rtype: Devuelve una lista de los datos virtuales, caso contrario devuelve el error generado
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
            filters['cliente'] = pk

            # Serializar los datos
            query = DatosVirtualesClientes.objects.filter(**filters).order_by('-created_at')
            serializer = DatosVirtualesClientesSerializer(query[offset:limit], many=True)
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
def datosVirtuales_findOne(request, pk):
    """
    Este metodo sirve para obtener un dato virtual de la tabla datos virtuales de la base datos mdm
    @type pk: el campo pk recibe el id del cliente
    @type request: El campo request no recibe nada
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
            datosVirtuales = DatosVirtualesClientes.objects.get(pk=pk, state=1)
        except DatosVirtualesClientes.DoesNotExist:
            err = {"error": "No existe"}
            createLog(logModel, err, logExcepcion)
            return Response(err, status=status.HTTP_404_NOT_FOUND)
        # tomar el dato
        if request.method == 'GET':
            serializer = DatosVirtualesClientesSerializer(datosVirtuales)
            createLog(logModel, serializer.data, logTransaccion)
            return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        err = {"error": 'Un error ha ocurrido: {}'.format(e)}
        createLog(logModel, err, logExcepcion)
        return Response(err, status=status.HTTP_400_BAD_REQUEST)


# CREAR
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def datosVirtuales_create(request):
    """
    Este metodo sirve para crear los datos virtuales de la tabla datos virtuales de la base datos mdm
    @type request: El campo request recibe los campos de la tabla datos virtuales
    @rtype: Devuelve el registro creado,caso contrario devuelve el error generado
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

            serializer = DatosVirtualesClientesSerializer(data=request.data)
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
def datosVirtuales_update(request, pk):
    """
    Este metodo sirve para actualizar los datos virtuales de la tabla datos virtuales de la base datos mdm
    @type pk: El campo pk recibe el id del cliente
    @type request: El campo request recibe los campos de la tabla datos virtuales
    @rtype: DEvuelve el registro actualizado, caso contrario devuelve el error generado
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
            datosVirtuales = DatosVirtualesClientes.objects.get(pk=pk, state=1)
        except DatosVirtualesClientes.DoesNotExist:
            errorNoExiste = {'error': 'No existe'}
            createLog(logModel, errorNoExiste, logExcepcion)
            return Response(status=status.HTTP_404_NOT_FOUND)
        if request.method == 'POST':
            now = timezone.localtime(timezone.now())
            request.data['updated_at'] = str(now)
            if 'created_at' in request.data:
                request.data.pop('created_at')
            serializer = DatosVirtualesClientesSerializer(datosVirtuales, data=request.data, partial=True)
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
def datosVirtuales_delete(request, pk):
    """
    Este metodo sirve para borrar los datos virtuales de la tabla datos virtuales de la base datos mdm
    @type pk: El campo pk recibe el id del datos virtuales
    @type request: El campo request no recibe nada
    @rtype: Devuelve el registro borrado, caso contrario devuelve el error generado
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
            datosVirtuales = DatosVirtualesClientes.objects.get(pk=pk, state=1)
        except DatosVirtualesClientes.DoesNotExist:
            err = {"error": "No existe"}
            createLog(logModel, err, logExcepcion)
            return Response(err, status=status.HTTP_404_NOT_FOUND)
        # tomar el dato
        if request.method == 'DELETE':
            serializer = DatosVirtualesClientesSerializer(datosVirtuales,
                                                          data={'state': '0', 'updated_at': str(nowDate)}, partial=True)
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
