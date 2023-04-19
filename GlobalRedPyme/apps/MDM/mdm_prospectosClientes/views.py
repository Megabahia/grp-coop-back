from apps.MDM.mdm_prospectosClientes.models import ProspectosClientes
from apps.MDM.mdm_prospectosClientes.serializers import ProspectosClientesSerializer, ProspectosClientesListarSerializer, ProspectosClienteImagenSerializer, ProspectosClientesSearchSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from datetime import datetime
from datetime import timedelta
#excel
import openpyxl
#logs
from apps.CENTRAL.central_logs.methods import createLog,datosTipoLog, datosProspectosClientes
#declaracion variables log
datosAux=datosProspectosClientes()
datosTipoLogAux=datosTipoLog()
#asignacion datos modulo
logModulo=datosAux['modulo']
logApi=datosAux['api']
#asignacion tipo de datos
logTransaccion=datosTipoLogAux['transaccion']
logExcepcion=datosTipoLogAux['excepcion']
#CRUD PROSPECTO CLIENTES
#LISTAR TODOS
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def prospecto_cliente_list(request):
    timezone_now = timezone.localtime(timezone.now())
    logModel = {
        'endPoint': logApi+'list/',
        'modulo':logModulo,
        'tipo' : logExcepcion,
        'accion' : 'LEER',
        'fechaInicio' : str(timezone_now),
        'dataEnviada' : '{}',
        'fechaFin': str(timezone_now),
        'dataRecibida' : '{}'
    }
    if request.method == 'POST':
        try:
            logModel['dataEnviada'] = str(request.data)
            #paginacion
            page_size=int(request.data['page_size'])
            page=int(request.data['page'])
            offset = page_size* page
            limit = offset + page_size
            #Filtros
            filters={"state":"1"}
            if 'canal' in request.data:
                if request.data['canal']!='':
                    filters['canal'] = str(request.data['canal'])
            if 'created_at' in request.data:
                if request.data['created_at']!='':
                    # Correccion de filtar por fechas importar timedelta
                    filters['created_at__lte'] = datetime.strptime(request.data['created_at'], "%Y-%m-%d").date() + timedelta(days=1)
            if 'nombreVendedor' in request.data:
                if request.data['nombreVendedor']!='':
                    filters['nombreVendedor'] = str(request.data['nombreVendedor'])
            if 'confirmacionProspecto' in request.data:
                if request.data['confirmacionProspecto']!='':
                    filters['confirmacionProspecto'] = str(request.data['confirmacionProspecto'])
            if 'empresa_id' in request.data:
                if request.data['empresa_id']!='':
                    filters['empresa_id'] = str(request.data['empresa_id'])
          
            #Serializar los datos
            query = ProspectosClientes.objects.filter(**filters).order_by('-created_at')
            serializer = ProspectosClientesListarSerializer(query[offset:limit], many=True)
            new_serializer_data={'cont': query.count(),
            'info':serializer.data}
            #envio de datos
            return Response(new_serializer_data,status=status.HTTP_200_OK)
        except Exception as e: 
            err={"error":'Un error ha ocurrido: {}'.format(e)}  
            createLog(logModel,err,logExcepcion)
            return Response(err, status=status.HTTP_400_BAD_REQUEST) 
#Buscar prospecto
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def prospecto_cliente_search(request):
    timezone_now = timezone.localtime(timezone.now())
    logModel = {
        'endPoint': logApi+'list/',
        'modulo':logModulo,
        'tipo' : logExcepcion,
        'accion' : 'LEER',
        'fechaInicio' : str(timezone_now),
        'dataEnviada' : '{}',
        'fechaFin': str(timezone_now),
        'dataRecibida' : '{}'
    }
    if request.method == 'POST':
        try:
            logModel['dataEnviada'] = str(request.data)
            #paginacion
            page_size=20
            page=0
            offset = page_size* page
            limit = offset + page_size
            #Filtros
            filters={"state":"1"}
            if 'nombreCompleto' in request.data:
                if request.data['nombreCompleto']!='':
                    filters['nombreCompleto__icontains'] = str(request.data['nombreCompleto'])
            if 'identificacion' in request.data:
                if request.data['identificacion']!='':
                    filters['identificacion'] = str(request.data['identificacion'])
            if 'telefono' in request.data:
                if request.data['telefono']!='':
                    filters['telefono'] = str(request.data['telefono'])
          
            #Serializar los datos
            query = ProspectosClientes.objects.filter(**filters).order_by('-created_at')
            serializer = ProspectosClientesSearchSerializer(query[offset:limit], many=True)
            new_serializer_data={'cont': query.count(),
            'info':serializer.data}
            #envio de datos
            return Response(new_serializer_data,status=status.HTTP_200_OK)
        except Exception as e: 
            err={"error":'Un error ha ocurrido: {}'.format(e)}  
            createLog(logModel,err,logExcepcion)
            return Response(err, status=status.HTTP_400_BAD_REQUEST) 

#ENCONTRAR UNO
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def prospecto_cliente_findOne(request, pk):
    timezone_now = timezone.localtime(timezone.now())
    logModel = {
        'endPoint': logApi+'listOne/',
        'modulo':logModulo,
        'tipo' : logExcepcion,
        'accion' : 'LEER',
        'fechaInicio' : str(timezone_now),
        'dataEnviada' : '{}',
        'fechaFin': str(timezone_now),
        'dataRecibida' : '{}'
    }
    try:
        try:
            query = ProspectosClientes.objects.get(pk=pk, state=1)
        except ProspectosClientes.DoesNotExist:
            err={"error":"No existe"}  
            createLog(logModel,err,logExcepcion)
            return Response(err,status=status.HTTP_404_NOT_FOUND)
        #tomar el dato
        if request.method == 'GET':
            serializer = ProspectosClientesSerializer(query)
            createLog(logModel,serializer.data,logTransaccion)
            return Response(serializer.data,status=status.HTTP_200_OK)
    except Exception as e: 
            err={"error":'Un error ha ocurrido: {}'.format(e)}  
            createLog(logModel,err,logExcepcion)
            return Response(err, status=status.HTTP_400_BAD_REQUEST)

#CREAR
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def prospecto_cliente_create(request):
    request.POST._mutable = True
    timezone_now = timezone.localtime(timezone.now())
    logModel = {
        'endPoint': logApi+'create/',
        'modulo':logModulo,
        'tipo' : logExcepcion,
        'accion' : 'CREAR',
        'fechaInicio' : str(timezone_now),
        'dataEnviada' : '{}',
        'fechaFin': str(timezone_now),
        'dataRecibida' : '{}'
    }
    if request.method == 'POST':
        try:
            prospectoCliente = ProspectosClientes.objects.filter(identificacion=request.data['identificacion']).first()
            if prospectoCliente is not None:
                data={'error':'Ya existe un prospecto cliente con esa identificación.'}
                return Response(data, status=status.HTTP_400_BAD_REQUEST)
            logModel['dataEnviada'] = str(request.data)
            request.data['created_at'] = str(timezone_now)
            if 'updated_at' in request.data:
                request.data.pop('updated_at')
            
            request.data['nombreCompleto'] = request.data['nombres'] + ' ' + request.data['apellidos']
        
            serializer = ProspectosClientesSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                createLog(logModel,serializer.data,logTransaccion)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            createLog(logModel,serializer.errors,logExcepcion)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e: 
            err={"error":'Un error ha ocurrido: {}'.format(e)}  
            createLog(logModel,err,logExcepcion)
            return Response(err, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def prospecto_cliente_update(request, pk):
    request.POST._mutable = True
    timezone_now = timezone.localtime(timezone.now())
    logModel = {
        'endPoint': logApi+'update/',
        'modulo':logModulo,
        'tipo' : logExcepcion,
        'accion' : 'ESCRIBIR',
        'fechaInicio' : str(timezone_now),
        'dataEnviada' : '{}',
        'fechaFin': str(timezone_now),
        'dataRecibida' : '{}'
    }
    try:
        # prospectoCliente = ProspectosClientes.objects.filter(identificacion=request.data['identificacion']).exclude(pk=pk).first()
        # if prospectoCliente is not None:
        #     data={'error':'Ya existe un prospecto cliente con esa identificación.'}
        #     return Response(data, status=status.HTTP_400_BAD_REQUEST)
        try:
            logModel['dataEnviada'] = str(request.data)
            query = ProspectosClientes.objects.get(pk=pk, state=1)
        except ProspectosClientes.DoesNotExist:
            errorNoExiste={'error':'No existe'}
            createLog(logModel,errorNoExiste,logExcepcion)
            return Response(status=status.HTTP_404_NOT_FOUND)
        if request.method == 'POST':
            now = timezone.localtime(timezone.now())
            request.data['updated_at'] = str(now)
            if 'created_at' in request.data:
                request.data.pop('created_at')
            if 'nombres' in request.data:
                request.data['nombreCompleto'] = request.data['nombres'] + ' ' + request.data['apellidos']
            serializer = ProspectosClientesSerializer(query, data=request.data,partial=True)
            if serializer.is_valid():
                serializer.save()
                createLog(logModel,serializer.data,logTransaccion)
                return Response(serializer.data)
            createLog(logModel,serializer.errors,logExcepcion)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e: 
        err={"error":'Un error ha ocurrido: {}'.format(e)}  
        createLog(logModel,err,logExcepcion)
        return Response(err, status=status.HTTP_400_BAD_REQUEST) 

#ELIMINAR
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def prospecto_cliente_delete(request, pk):
    nowDate = timezone.localtime(timezone.now())
    logModel = {
        'endPoint': logApi+'delete/',
        'modulo':logModulo,
        'tipo' : logExcepcion,
        'accion' : 'BORRAR',
        'fechaInicio' : str(nowDate),
        'dataEnviada' : '{}',
        'fechaFin': str(nowDate),
        'dataRecibida' : '{}'
    }
    try:
        try:
            query = ProspectosClientes.objects.get(pk=pk, state=1)
        except ProspectosClientes.DoesNotExist:
            err={"error":"No existe"}  
            createLog(logModel,err,logExcepcion)
            return Response(err,status=status.HTTP_404_NOT_FOUND)
            return Response(status=status.HTTP_404_NOT_FOUND)
        #tomar el dato
        if request.method == 'DELETE':
            serializer = ProspectosClientesSerializer(query, data={'state': '0','updated_at':str(nowDate)},partial=True)
            if serializer.is_valid():
                serializer.save()
                createLog(logModel,serializer.data,logTransaccion)
                return Response(serializer.data,status=status.HTTP_200_OK)
            createLog(logModel,serializer.errors,logExcepcion)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e: 
        err={"error":'Un error ha ocurrido: {}'.format(e)}  
        createLog(logModel,err,logExcepcion)
        return Response(err, status=status.HTTP_400_BAD_REQUEST) 

# SUBIR IMAGEN
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def prospectosclientesImagen_update(request, pk):
    timezone_now = timezone.localtime(timezone.now())
    logModel = {
        'endPoint': logApi+'update/imagen/',
        'modulo':logModulo,
        'tipo' : logExcepcion,
        'accion' : 'ESCRIBIR',
        'fechaInicio' : str(timezone_now),
        'dataEnviada' : '{}',
        'fechaFin': str(timezone_now),
        'dataRecibida' : '{}'
    }
    try:
        try:
            logModel['dataEnviada'] = str(request.data)
            query = ProspectosClientes.objects.get(pk=pk, state=1)
        except ProspectosClientes.DoesNotExist:
            errorNoExiste={'error':'No existe'}
            createLog(logModel,errorNoExiste,logExcepcion)
            return Response(status=status.HTTP_404_NOT_FOUND)
        if request.method == 'POST':
            now = timezone.localtime(timezone.now())
            request.data['updated_at'] = str(now)
            if 'created_at' in request.data:
                request.data.pop('created_at')
            serializer = ProspectosClienteImagenSerializer(query, data=request.data,partial=True)
            if serializer.is_valid():
                serializer.save()
                createLog(logModel,serializer.data,logTransaccion)
                return Response(serializer.data)
            createLog(logModel,serializer.errors,logExcepcion)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e: 
        err={"error":'Un error ha ocurrido: {}'.format(e)}  
        createLog(logModel,err,logExcepcion)
        return Response(err, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def uploadCSV_crearProspectosClientes(request):
    contValidos=0
    contInvalidos=0
    contTotal=0
    errores=[]
    try:
        if request.method == 'POST':
            first = True    #si tiene encabezado
            uploaded_file = request.FILES['documento']
            lines = uploaded_file.readlines()
            for line in lines:
                contTotal+=1
                if first:
                    line.decode(encoding='utf-8').split(",")
                    first = False
                    continue
                else:
                    dato = line.decode(encoding='utf-8').split(",")
                    if len(dato)==18:
                        resultadoInsertar=insertarDato_prospectoCliente(dato)
                        if resultadoInsertar!='Dato insertado correctamente':
                            contInvalidos+=1   
                            errores.append({"error":"Error en la línea "+str(contTotal)+": "+str(resultadoInsertar)})
                        else:
                            contValidos+=1
                    else:
                        contInvalidos+=1    
                        errores.append({"error":"Error en la línea "+str(contTotal)+": la fila tiene un tamaño incorrecto ("+str(len(dato))+")"}) 

            result={"mensaje":"La Importación se Realizo Correctamente",
            "correctos":contValidos,
            "incorrectos":contInvalidos,
            "errores":errores
            }
            return Response(result, status=status.HTTP_201_CREATED)
    except Exception as e:
        err={"error":'Error verifique el archivo, un error ha ocurrido: {}'.format(e)}  
        return Response(err, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def uploadEXCEL_crearProspectosClientes(request):
    contValidos=0
    contInvalidos=0
    contTotal=0
    errores=[]
    try:
        if request.method == 'POST':
            first = True    #si tiene encabezado
            uploaded_file = request.FILES['documento']
            # you may put validations here to check extension or file size
            wb = openpyxl.load_workbook(uploaded_file)
            # getting a particular sheet by name out of many sheets
            worksheet = wb["prospectosClientes"]
            lines = list()
        for row in worksheet.iter_rows():
            row_data = list()
            for cell in row:
                row_data.append(str(cell.value))
            lines.append(row_data)

        for dato in lines:
            contTotal+=1
            if first:
                first = False
                continue
            else:
                if len(dato)==18:
                    resultadoInsertar=insertarDato_prospectoCliente(dato)
                    if resultadoInsertar!='Dato insertado correctamente':
                        contInvalidos+=1 
                        errores.append({"error":"Error en la línea "+str(contTotal)+": "+str(resultadoInsertar)})
                    else:
                        contValidos+=1
                else:
                    contInvalidos+=1    
                    errores.append({"error":"Error en la línea "+str(contTotal)+": la fila tiene un tamaño incorrecto ("+str(len(dato))+")"}) 

        result={"mensaje":"La Importación se Realizo Correctamente",
        "correctos":contValidos,
        "incorrectos":contInvalidos,
        "errores":errores
        }
        return Response(result, status=status.HTTP_201_CREATED)

    except Exception as e:
        err={"error":'Error verifique el archivo, un error ha ocurrido: {}'.format(e)}  
        return Response(err, status=status.HTTP_400_BAD_REQUEST)

def insertarDato_prospectoCliente(dato):
    try:
        timezone_now = timezone.localtime(timezone.now())
        data={}
        data['nombres'] = str(dato[0])
        data['apellidos'] = dato[1]
        data['telefono'] = dato[2]
        data['tipoCliente'] = dato[3]
        data['whatsapp'] = dato[4]
        data['facebook'] = dato[5]
        data['twitter'] = dato[6]
        data['instagram'] = dato[7]
        data['correo1'] = dato[8]
        data['correo2'] = dato[9]
        data['ciudad'] = dato[10]
        data['canal'] = dato[11]
        data['codigoProducto'] = dato[12]
        data['nombreProducto'] = dato[13]
        data['precio'] = dato[14]
        data['tipoPrecio'] = dato[15]
        data['nombreVendedor'] = dato[16]
        data['confirmacionProspecto'] = dato[17]
        data['created_at'] = str(timezone_now)
        #inserto el dato con los campos requeridos
        ProspectosClientes.objects.create(**data)
        return 'Dato insertado correctamente'
    except Exception as e:
        return str(e)
