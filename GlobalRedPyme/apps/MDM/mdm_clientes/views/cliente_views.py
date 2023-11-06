from ..models import Clientes, DatosVirtualesClientes
from ...mdm_prospectosClientes.models import ProspectosClientes
from ...mdm_facturas.models import FacturasEncabezados
from ..models import DatosVirtualesClientes
from ..serializers import DatosVirtualesClientesSerializer
from ..serializers import ClientesSerializer, ClientesListarSerializer, ClienteImagenSerializer, \
    ClientesUpdateSerializer, ClientePrediccionSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
# excel
import openpyxl
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


# CRUD CLIENTES
# LISTAR TODOS
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def cliente_list(request):
    """
    Metodo sirve para listar los clientes de la tabla clientes de la base datos mdm
    @type request: El campo request recibe los campos nombreCompleto, cedula, inicio, fin, empresa_id
    @rtype: DEvuelve una listar de los clientes, caso contrario devuelve el error generado
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
            if 'nombreCompleto' in request.data:
                if request.data['nombreCompleto'] != '':
                    filters['nombreCompleto__icontains'] = str(request.data['nombreCompleto'])
            # if 'apellidos' in request.data:
            #     if request.data['apellidos']!='':
            #         filters['apellidos__icontains'] = str(request.data['apellidos'])
            if 'cedula' in request.data:
                if request.data['cedula'] != '':
                    filters['cedula'] = str(request.data['cedula'])
            if 'inicio' and 'fin' in request.data:
                # if request.data['inicio'] !='':
                #     filters['created_at__startswith'] = str(request.data['inicio'])
                if request.data['inicio'] and request.data['fin'] != '':
                    filters['created_at__range'] = [str(request.data['inicio']), str(request.data['fin'])]
            if 'empresa_id' in request.data:
                if request.data['empresa_id'] != '':
                    filters['empresa_id'] = request.data['empresa_id']

            # Serializar los datos
            query = Clientes.objects.filter(**filters).order_by('-created_at')
            serializer = ClientesListarSerializer(query[offset:limit], many=True)
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
def cliente_findOne(request, pk):
    """
    Metodo de obtener un cliente de la tabla de clientes de la base datos mdm
    @type pk: El campo pk es el id del cliente
    @type request: El campo request no recibe nada
    @rtype: Devuelve el registro del cliente, caso contrario devuelve el error generado
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
            query = Clientes.objects.get(pk=pk, state=1)
        except Clientes.DoesNotExist:
            err = {"error": "No existe"}
            createLog(logModel, err, logExcepcion)
            return Response(err, status=status.HTTP_404_NOT_FOUND)
        # tomar el dato
        if request.method == 'GET':
            serializer = ClientesSerializer(query)
            createLog(logModel, serializer.data, logTransaccion)
            return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        err = {"error": 'Un error ha ocurrido: {}'.format(e)}
        createLog(logModel, err, logExcepcion)
        return Response(err, status=status.HTTP_400_BAD_REQUEST)


# ENCONTRAR UNO
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def cliente_findOne_cedula(request):
    """
    Este metodo obtiene un cliente con su cedula de la tabla cliente de la base datos mdm
    @type request: El campo request recibe la cedula
    @rtype: DEvuevlve el registro que coicide, caso contrario devuevl el error
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
            query = Clientes.objects.get(cedula=str(request.data['cedula']), state=1)
        except Clientes.DoesNotExist:
            err = {"error": "No existe"}
            createLog(logModel, err, logExcepcion)
            return Response(err, status=status.HTTP_404_NOT_FOUND)
        # tomar el dato
        if request.method == 'POST':
            serializer = ClientesSerializer(query)
            createLog(logModel, serializer.data, logTransaccion)
            return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        err = {"error": 'Un error ha ocurrido: {}'.format(e)}
        createLog(logModel, err, logExcepcion)
        return Response(err, status=status.HTTP_400_BAD_REQUEST)


# ENCONTRAR UNO
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def cliente_findOne_telefono(request):
    """
    Este metodo sirve para buscar por telefono de la tabla clientes de la base datos mdm
    @type request: El campo request recibe el telefono
    @rtype: Devuelve el registro que coicida, caso contrario devuelve el error generado
    """
    timezone_now = timezone.localtime(timezone.now())
    logModel = {
        'endPoint': logApi + 'listOne/telefono/',
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
            query = Clientes.objects.get(telefono=str(request.data['telefono']), state=1)
        except Clientes.DoesNotExist:
            err = {"error": "No existe"}
            createLog(logModel, err, logExcepcion)
            return Response(err, status=status.HTTP_404_NOT_FOUND)
        # tomar el dato
        if request.method == 'POST':
            serializer = ClientesSerializer(query)
            createLog(logModel, serializer.data, logTransaccion)
            return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        err = {"error": 'Un error ha ocurrido: {}'.format(e)}
        createLog(logModel, err, logExcepcion)
        return Response(err, status=status.HTTP_400_BAD_REQUEST)


# CREAR
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def cliente_create(request):
    """
    El metodo sirve para crear un cliente de la tabla cliente de la base datos mdm
    @type request: El campo request recibe los campos de la tabla clientes
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
            request.data['nombreCompleto'] = str(request.data['nombres']) + " " + str(request.data['apellidos'])
            if 'updated_at' in request.data:
                request.data.pop('updated_at')

            serializer = ClientesSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                prospectoCliente = ProspectosClientes.objects.filter(identificacion=request.data['cedula'],
                                                                     state=1).first()
                if prospectoCliente is not None:
                    prospectoCliente.state = 0
                    prospectoCliente.save()
                    DatosVirtualesClientes.objects.create(cliente_id=serializer.data['id'],
                                                          tipoContacto="Whatsapp personal",
                                                          informacion=prospectoCliente.whatsapp, icono='phone')
                    DatosVirtualesClientes.objects.create(cliente_id=serializer.data['id'],
                                                          tipoContacto="Facebook personal",
                                                          informacion=prospectoCliente.facebook, icono='facebook')
                    DatosVirtualesClientes.objects.create(cliente_id=serializer.data['id'],
                                                          tipoContacto="Instagram personal",
                                                          informacion=prospectoCliente.instagram, icono='instagram')
                    DatosVirtualesClientes.objects.create(cliente_id=serializer.data['id'],
                                                          tipoContacto="Twitter personal",
                                                          informacion=prospectoCliente.twitter, icono='twitter')
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
def cliente_update(request, pk):
    """
    Este metodo sirve para actualizar el cliente de la tabla clientes de la mdm
    @type pk: El campo pk es el id del cliente
    @type request: El campo request recibe los campos de la tabla clientes
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
            query = Clientes.objects.get(pk=pk, state=1)
        except Clientes.DoesNotExist:
            errorNoExiste = {'error': 'No existe'}
            createLog(logModel, errorNoExiste, logExcepcion)
            return Response(status=status.HTTP_404_NOT_FOUND)
        if request.method == 'POST':
            now = timezone.localtime(timezone.now())
            request.data['updated_at'] = str(now)
            if 'created_at' in request.data:
                request.data.pop('created_at')
            serializer = ClientesUpdateSerializer(query, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                prospectoCliente = ProspectosClientes.objects.filter(identificacion=request.data['cedula'],
                                                                     state=1).first()
                if prospectoCliente is not None:
                    prospectoCliente.state = 0
                    prospectoCliente.save()

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
def cliente_delete(request, pk):
    """
    Este metodo sirve para borrar el cliente de la tabla clientes de la base datos mdm
    @type pk: El campo pk es el id del cliente
    @type request: El campo request no recibe nada
    @rtype: Devuelve el registro borrado, caso contrario devuelve error generado
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
            query = Clientes.objects.get(pk=pk, state=1)
        except Clientes.DoesNotExist:
            err = {"error": "No existe"}
            createLog(logModel, err, logExcepcion)
            return Response(err, status=status.HTTP_404_NOT_FOUND)
        # tomar el dato
        if request.method == 'DELETE':
            serializer = ClientesSerializer(query, data={'state': '0', 'updated_at': str(nowDate)}, partial=True)
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
def clienteImagen_update(request, pk):
    """
    Este metodo sirve para actualizar la imagen del cliente de la tabla clientes de la base datos mdm
    @type pk: El campo pk recibe el id del cliente
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
            query = Clientes.objects.get(pk=pk, state=1)
        except Clientes.DoesNotExist:
            errorNoExiste = {'error': 'No existe'}
            createLog(logModel, errorNoExiste, logExcepcion)
            return Response(status=status.HTTP_404_NOT_FOUND)
        if request.method == 'POST':
            now = timezone.localtime(timezone.now())
            request.data['updated_at'] = str(now)
            if 'created_at' in request.data:
                request.data.pop('created_at')
            serializer = ClienteImagenSerializer(query, data=request.data, partial=True)
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


# METODO SUBIR ARCHIVOS CSV
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def uploadCSV_crearClientes(request):
    """
    Este metodo sirve para cargar a clientes a la tabla clientes de la base datos mdm
    @type request: El campo request recibe el archivo
    @rtype: Devuelve la cantidad de fila correctas, erroneas
    """
    contValidos = 0
    contInvalidos = 0
    contTotal = 0
    errores = []
    try:
        if request.method == 'POST':
            first = True  # si tiene encabezado
            uploaded_file = request.FILES['documento']
            lines = uploaded_file.readlines()
            for line in lines:
                contTotal += 1
                if first:
                    line.decode(encoding='utf-8').split(",")
                    first = False
                    continue
                else:
                    dato = line.decode(encoding='utf-8').split(",")
                    if len(dato) == 25:
                        resultadoInsertar = insertarDato_cliente(dato)
                        if resultadoInsertar != 'Dato insertado correctamente':
                            contInvalidos += 1
                            errores.append(
                                {"error": "Error en la línea " + str(contTotal) + ": " + str(resultadoInsertar)})
                        else:
                            contValidos += 1
                    else:
                        contInvalidos += 1
                        errores.append({"error": "Error en la línea " + str(
                            contTotal) + ": la fila tiene un tamaño incorrecto (" + str(len(dato)) + ")"})

            result = {"mensaje": "La Importación se Realizo Correctamente",
                      "correctos": contValidos,
                      "incorrectos": contInvalidos,
                      "errores": errores
                      }
            return Response(result, status=status.HTTP_201_CREATED)
    except Exception as e:
        err = {"error": 'Error verifique el archivo, un error ha ocurrido: {}'.format(e)}
        return Response(err, status=status.HTTP_400_BAD_REQUEST)


# METODO SUBIR ARCHIVOS EXCEL
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def uploadEXCEL_crearClientes(request):
    """
    Este metodo sirve para cargar a clientes a la tabla clientes de la base datos mdm
    @type request: El campo request recibe el archivo
    @rtype: Devuelve la cantidad de fila correctas, erroneas
    """
    contValidos = 0
    contInvalidos = 0
    contTotal = 0
    errores = []
    try:
        if request.method == 'POST':
            first = True  # si tiene encabezado
            uploaded_file = request.FILES['documento']
            # you may put validations here to check extension or file size
            wb = openpyxl.load_workbook(uploaded_file)
            # getting a particular sheet by name out of many sheets
            worksheet = wb["Clientes"]
            lines = list()
        for row in worksheet.iter_rows():
            row_data = list()
            for cell in row:
                row_data.append(str(cell.value))
            lines.append(row_data)

        for dato in lines:
            contTotal += 1
            if first:
                first = False
                continue
            else:
                if len(dato) == 25:
                    resultadoInsertar = insertarDato_cliente(dato)
                    if resultadoInsertar != 'Dato insertado correctamente':
                        contInvalidos += 1
                        errores.append({"error": "Error en la línea " + str(contTotal) + ": " + str(resultadoInsertar)})
                    else:
                        contValidos += 1
                else:
                    contInvalidos += 1
                    errores.append({"error": "Error en la línea " + str(
                        contTotal) + ": la fila tiene un tamaño incorrecto (" + str(len(dato)) + ")"})

        result = {"mensaje": "La Importación se Realizo Correctamente",
                  "correctos": contValidos,
                  "incorrectos": contInvalidos,
                  "errores": errores
                  }
        return Response(result, status=status.HTTP_201_CREATED)

    except Exception as e:
        err = {"error": 'Error verifique el archivo, un error ha ocurrido: {}'.format(e)}
        return Response(err, status=status.HTTP_400_BAD_REQUEST)


# INSERTAR DATOS EN LA BASE INDIVIDUAL
def insertarDato_cliente(dato):
    """
    Este metodo sirve para insertar el cliente en la tabla clientes de la base datos mdm
    @type dato: El campo dato recibe la fila del documento
    @rtype: DEvuelve los errores si existen
    """
    try:
        timezone_now = timezone.localtime(timezone.now())
        data = {}
        data['tipoCliente'] = dato[0].replace('"', "") if dato[0].replace('"', "") != "NULL" else None
        data['cedula'] = dato[1].replace('"', "") if dato[1] != "NULL" else None
        data['nombreCompleto'] = dato[2].replace('"', "") + " " + dato[3].replace('"', "") if dato[
                                                                                                  2] != "NULL" else None
        data['nombres'] = dato[2].replace('"', "") if dato[2] != "NULL" else None
        data['apellidos'] = dato[3].replace('"', "") if dato[3] != "NULL" else None
        data['genero'] = dato[4].replace('"', "") if dato[4] != "NULL" else None
        data['nacionalidad'] = dato[5].replace('"', "") if dato[5] != "NULL" else None
        data['fechaNacimiento'] = dato[6].replace('"', "")[:10] if dato[6] != "NULL" else None
        data['edad'] = dato[7].replace('"', "") if dato[7] != "NULL" else None
        data['paisNacimiento'] = dato[8].replace('"', "") if dato[8] != "NULL" else None
        data['provinciaNacimiento'] = dato[9].replace('"', "") if dato[9] != "NULL" else None
        data['ciudadNacimiento'] = dato[10].replace('"', "") if dato[10] != "NULL" else None
        data['estadoCivil'] = dato[11].replace('"', "") if dato[11] != "NULL" else None
        data['paisResidencia'] = dato[12].replace('"', "") if dato[12] != "NULL" else None
        data['provinciaResidencia'] = dato[13].replace('"', "") if dato[13] != "NULL" else None
        data['ciudadResidencia'] = dato[14].replace('"', "") if dato[14] != "NULL" else None
        data['nivelEstudios'] = dato[15].replace('"', "") if dato[15] != "NULL" else None
        data['profesion'] = dato[16].replace('"', "") if dato[16] != "NULL" else None
        data['lugarTrabajo'] = dato[17].replace('"', "") if dato[17] != "NULL" else None
        data['paisTrabajo'] = dato[18].replace('"', "") if dato[18] != "NULL" else None
        data['provinciaTrabajo'] = dato[19].replace('"', "") if dato[19] != "NULL" else None
        data['ciudadTrabajo'] = dato[20].replace('"', "") if dato[20] != "NULL" else None
        data['mesesUltimoTrabajo'] = dato[21].replace('"', "") if dato[21] != "NULL" else None
        data['mesesTotalTrabajo'] = dato[22].replace('"', "") if dato[22] != "NULL" else None
        data['ingresosPromedioMensual'] = dato[23].replace('"', "") if dato[23] != "NULL" else None
        data['gastosPromedioMensual'] = dato[24].replace('"', "") if dato[24] != "NULL" else None
        data['created_at'] = str(timezone_now)
        # inserto el dato con los campos requeridos
        Clientes.objects.create(**data)
        return 'Dato insertado correctamente'
    except Exception as e:
        return str(e)


# ENCONTRAR CLIENTE POR FACTURA
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def cliente_by_factura_findOne(request, pk):
    """
    Este metodo sirve para consultar una factura por el cliente de la tabla facturas de la base datos mdp
    @type pk: el campo pk es el id de la factura
    @type request: El campo request no recibe nada
    @rtype: DEvuelve el cliente si encuentra la factura, caso contrario devuelve el error generado
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
            serializer = ClientePrediccionSerializer(query.cliente)
            query = DatosVirtualesClientes.objects.filter(cliente=query.cliente)
            datosVirtuales = DatosVirtualesClientesSerializer(query, many=True)
            data = {**serializer.data, 'datosVirtuales': datosVirtuales.data}
            createLog(logModel, data, logTransaccion)
            return Response(data, status=status.HTTP_200_OK)
    except Exception as e:
        err = {"error": 'Un error ha ocurrido: {}'.format(e)}
        createLog(logModel, err, logExcepcion)
        return Response(err, status=status.HTTP_400_BAD_REQUEST)


# ENCONTRAR CLIENTE POR PK
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def cliente_prediccionRefil_findOne(request, pk):
    """
    Este metodo sirve para buscar la predicion de refil de la tabla clientes de la base mdm
    @type pk: El campo pk es el id del cliente
    @type request: El campo request no recibe nada
    @rtype: DEvuelve una lista con las predicciones
    """
    timezone_now = timezone.localtime(timezone.now())
    logModel = {
        'endPoint': logApi + 'prediccionRefil/listOne/',
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
            query = Clientes.objects.get(pk=pk, state=1)
        except Clientes.DoesNotExist:
            err = {"error": "No existe"}
            createLog(logModel, err, logExcepcion)
            return Response(err, status=status.HTTP_404_NOT_FOUND)
        # tomar el dato
        if request.method == 'GET':
            serializer = ClientePrediccionSerializer(query)
            query = DatosVirtualesClientes.objects.filter(cliente=query)
            datosVirtuales = DatosVirtualesClientesSerializer(query, many=True)
            data = {**serializer.data, 'datosVirtuales': datosVirtuales.data}
            createLog(logModel, serializer.data, logTransaccion)
            return Response(data, status=status.HTTP_200_OK)
    except Exception as e:
        err = {"error": 'Un error ha ocurrido: {}'.format(e)}
        createLog(logModel, err, logExcepcion)
        return Response(err, status=status.HTTP_400_BAD_REQUEST)
