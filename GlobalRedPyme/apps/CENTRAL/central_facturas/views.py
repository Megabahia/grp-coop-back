from apps.CENTRAL.central_facturas.models import  Facturas
from apps.CENTRAL.central_facturas.serializers import (
    FacturasSerializer, ListFacturasSerializer, SubirFacturasSerializer
)
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
# ObjectId
from bson import ObjectId
#logs
from apps.CENTRAL.central_logs.methods import createLog,datosTipoLog, datosProductosMDP
#declaracion variables log
datosAux=datosProductosMDP()
datosTipoLogAux=datosTipoLog()
#asignacion datos modulo
logModulo=datosAux['modulo']
logApi=datosAux['api']
#asignacion tipo de datos
logTransaccion=datosTipoLogAux['transaccion']
logExcepcion=datosTipoLogAux['excepcion']
#CRUD PERSONAS
#LISTAR TODOS
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def facturas_list(request):
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

            if 'inicio' and 'fin' in request.data:
                if request.data['inicio'] and request.data['fin'] !='':
                    filters['created_at__range'] = [str(request.data['inicio']),str(request.data['fin'])]
            
            if 'user_id' in request.data:
                if request.data['user_id'] !='':
                    filters['user_id'] = str(request.data['user_id'])

            #Serializar los datos
            query = Facturas.objects.filter(**filters).order_by('-created_at')
            serializer = ListFacturasSerializer(query[offset:limit], many=True)
            new_serializer_data={'cont': query.count(),
            'info':serializer.data}
            #envio de datos
            return Response(new_serializer_data,status=status.HTTP_200_OK)
        except Exception as e: 
            err={"error":'Un error ha ocurrido: {}'.format(e)}  
            createLog(logModel,err,logExcepcion)
            return Response(err, status=status.HTTP_400_BAD_REQUEST)

#CREAR
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def facturas_create(request):
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
            logModel['dataEnviada'] = str(request.data)
            request.data['created_at'] = str(timezone_now)
            if 'updated_at' in request.data:
                request.data.pop('updated_at')
            
            serializer = FacturasSerializer(data=request.data)
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

#ENCONTRAR UNO
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def facturas_listOne(request, pk):
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
            # Creo un ObjectoId porque la primaryKey de mongo es ObjectId
            pk = ObjectId(pk)
            query = Facturas.objects.get(pk=pk, state=1)
        except Facturas.DoesNotExist:
            err={"error":"No existe"}  
            createLog(logModel,err,logExcepcion)
            return Response(err,status=status.HTTP_404_NOT_FOUND)
        #tomar el dato
        if request.method == 'GET':
            serializer = FacturasSerializer(query)
            createLog(logModel,serializer.data,logTransaccion)
            return Response(serializer.data,status=status.HTTP_200_OK)
    except Exception as e: 
            err={"error":'Un error ha ocurrido: {}'.format(e)}  
            createLog(logModel,err,logExcepcion)
            return Response(err, status=status.HTTP_400_BAD_REQUEST)

# ACTUALIZAR
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def facturas_update(request, pk):
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
        try:
            logModel['dataEnviada'] = str(request.data)
            # Creo un ObjectoId porque la primaryKey de mongo es ObjectId
            pk = ObjectId(pk)
            query = Facturas.objects.get(pk=pk, state=1)
        except Facturas.DoesNotExist:
            errorNoExiste={'error':'No existe'}
            createLog(logModel,errorNoExiste,logExcepcion)
            return Response(status=status.HTTP_404_NOT_FOUND)
        if request.method == 'POST':
            now = timezone.localtime(timezone.now())
            request.data['updated_at'] = str(now)
            if 'created_at' in request.data:
                request.data.pop('created_at')
            
            if 'urlFoto' in request.data:
                if request.data['urlFoto'] == '':
                    request.data.pop('urlFoto')
            
            if 'urlArchivo' in request.data:
                if request.data['urlArchivo'] == '':
                    request.data.pop('urlArchivo')
            
            serializer = FacturasSerializer(query, data=request.data,partial=True)
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
def facturas_delete(request, pk):
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
            # Creo un ObjectoId porque la primaryKey de mongo es ObjectId
            pk = ObjectId(pk)
            query = Facturas.objects.get(pk=pk, state=1)
        except Facturas.DoesNotExist:
            err={"error":"No existe"}  
            createLog(logModel,err,logExcepcion)
            return Response(err,status=status.HTTP_404_NOT_FOUND)
            return Response(status=status.HTTP_404_NOT_FOUND)
        #tomar el dato
        if request.method == 'DELETE':
            serializer = FacturasSerializer(query, data={'state': '0','updated_at':str(nowDate)},partial=True)
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


# SUBIR FACTURA
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def facturas_subirArchivo(request):
    timezone_now = timezone.localtime(timezone.now())
    logModel = {
        'endPoint': logApi+'subir/factura/',
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
            logModel['dataEnviada'] = str(request.data)
            request.data['created_at'] = str(timezone_now)
            if 'updated_at' in request.data:
                request.data.pop('updated_at')
            
            serializer = SubirFacturasSerializer(data=request.data)
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

