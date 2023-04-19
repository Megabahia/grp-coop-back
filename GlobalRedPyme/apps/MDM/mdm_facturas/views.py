from apps.MDM.mdm_facturas.models import FacturasEncabezados, FacturasDetalles
from apps.MDM.mdm_facturas.serializers import FacturasSerializer, FacturasDetallesSerializer, FacturasListarSerializer, FacturaSerializer, FacturasListarTablaSerializer
from apps.MDP.mdp_productos.models import Productos
from apps.MDM.mdm_clientes.models import Clientes
from apps.MDM.mdm_negocios.models import Negocios
from apps.MDO.mdo_prediccionCrosseling.serializers import PrediccionCrosselingSerializer
from apps.MDO.mdo_prediccionProductosNuevos.serializers import PrediccionProductosSerializer
from apps.MDO.mdo_prediccionRefil.serializers import PrediccionRefilSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from datetime import datetime
from django.core import serializers
#excel
import openpyxl
#logs
from apps.CENTRAL.central_logs.methods import createLog,datosTipoLog, datosFacturas
#declaracion variables log
datosAux=datosFacturas()
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
def factura_list(request):
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
            if 'negocio' in request.data:
                if request.data['negocio']!='':
                    filters['negocio'] = request.data['negocio']
            if 'cliente' in request.data:
                if request.data['cliente']!='':
                    filters['cliente'] = request.data['cliente']
            if 'empresa_id' in request.data:
                if request.data['empresa_id']!='':
                    filters['empresa_id'] = request.data['empresa_id']
            # if 'cedula' in request.data:
            #     if request.data['cedula']!='':
            #         filters['cedula'] = str(request.data['cedula'])
            # if 'inicio' and 'fin' in request.data:                
            #     # if request.data['inicio'] !='':
            #     #     filters['created_at__startswith'] = str(request.data['inicio'])
            #     if request.data['inicio'] and request.data['fin'] !='':
            #         filters['created_at__range'] = [str(request.data['inicio']),str(request.data['fin'])]            
          
            #Serializar los datos
            query = FacturasEncabezados.objects.filter(**filters).order_by('-created_at')
            serializer = FacturasListarSerializer(query[offset:limit], many=True)
            new_serializer_data={'cont': query.count(),
            'info':serializer.data}
            #envio de datos
            return Response(new_serializer_data,status=status.HTTP_200_OK)
        except Exception as e: 
            err={"error":'Un error ha ocurrido: {}'.format(e)}  
            createLog(logModel,err,logExcepcion)
            return Response(err, status=status.HTTP_400_BAD_REQUEST) 
#LISTAR TODOS NEGOCIOS
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def factura_list_negocio(request):
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
            filters['negocio__isnull'] = False       
            if 'inicio' and 'fin' in request.data:
                if request.data['inicio'] and request.data['fin'] !='':
                    filters['created_at__range'] = [str(request.data['inicio']),str(request.data['fin'])]   
            if 'empresa_id' in request.data:
                if request.data['empresa_id']!='':
                    filters['empresa_id'] = request.data['empresa_id']
          
            #Serializar los datos
            query = FacturasEncabezados.objects.filter(**filters).order_by('-created_at')
            serializer = FacturasListarSerializer(query[offset:limit], many=True)
            new_serializer_data={'cont': query.count(),
            'info':serializer.data}
            #envio de datos
            return Response(new_serializer_data,status=status.HTTP_200_OK)
        except Exception as e: 
            err={"error":'Un error ha ocurrido: {}'.format(e)}  
            createLog(logModel,err,logExcepcion)
            return Response(err, status=status.HTTP_400_BAD_REQUEST) 

#LISTAR TODOS CLIENTES
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def factura_list_cliente(request):
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
            filters['cliente__isnull'] = False    
            if 'inicio' and 'fin' in request.data:
                if request.data['inicio'] and request.data['fin'] !='':
                    filters['created_at__range'] = [str(request.data['inicio']),str(request.data['fin'])]   
            if 'empresa_id' in request.data:
                if request.data['empresa_id']!='':
                    filters['empresa_id'] = request.data['empresa_id']
          
            #Serializar los datos
            query = FacturasEncabezados.objects.filter(**filters).order_by('-created_at')
            serializer = FacturasListarSerializer(query[offset:limit], many=True)
            new_serializer_data={'cont': query.count(),
            'info':serializer.data}
            #envio de datos
            return Response(new_serializer_data,status=status.HTTP_200_OK)
        except Exception as e: 
            err={"error":'Un error ha ocurrido: {}'.format(e)}  
            createLog(logModel,err,logExcepcion)
            return Response(err, status=status.HTTP_400_BAD_REQUEST) 
#LISTAR TODOS CLIENTE GRAFICA
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def factura_list_todos_rango_fecha_cliente_grafica(request):
    timezone_now = timezone.localtime(timezone.now())
    logModel = {
        'endPoint': logApi+'list/cliente/grafica/',
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
            
            query = FacturasEncabezados.objects.raw('''
            SELECT id,YEAR(created_at) anio,MONTH(created_at) mes , COUNT(*) cantidad FROM vittoria_mdm.mdm_facturas_facturasencabezados 
            WHERE  created_at between %s AND %s AND cliente_id is not null AND state = 1
            GROUP BY MONTH (created_at), YEAR(created_at) ORDER BY MONTH (created_at);''',[str(request.data['inicio']),str(request.data['fin'])])
            #Serializar los datos
            data = []
            for raw in query:
                data.append({'anio': raw.anio,'mes': raw.mes,'cantidad': raw.cantidad})
            #envio de datos
            return Response(data,status=status.HTTP_200_OK)
        except Exception as e: 
            err={"error":'Un error ha ocurrido: {}'.format(e)}  
            createLog(logModel,err,logExcepcion)
            return Response(err, status=status.HTTP_400_BAD_REQUEST) 
#LISTAR TODOS CLIENTE EN ESPECIFICO
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def factura_list_todos_rango_fecha_negocio_grafica(request):
    timezone_now = timezone.localtime(timezone.now())
    logModel = {
        'endPoint': logApi+'list/negocio/grafica',
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
            
            query = FacturasEncabezados.objects.raw('''
            SELECT id,YEAR(created_at) anio,MONTH(created_at) mes , COUNT(*) cantidad FROM vittoria_mdm.mdm_facturas_facturasencabezados 
            WHERE  created_at between %s AND %s AND negocio_id is not null AND state = 1
            GROUP BY MONTH (created_at), YEAR(created_at) ORDER BY MONTH (created_at);''',[str(request.data['inicio']),str(request.data['fin'])])
            #Serializar los datos
            data = []
            for raw in query:
                data.append({'anio': raw.anio,'mes': raw.mes,'cantidad': raw.cantidad})
            #envio de datos
            return Response(data,status=status.HTTP_200_OK)
        except Exception as e: 
            err={"error":'Un error ha ocurrido: {}'.format(e)}  
            createLog(logModel,err,logExcepcion)
            return Response(err, status=status.HTTP_400_BAD_REQUEST) 

#LISTAR TODOS CLIENTE EN ESPECIFICO
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def factura_list_rango_fecha_cliente(request,pk):
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
            filters['cliente__isnull'] = False    
            filters['cliente'] = pk    
            if 'inicio' and 'fin' in request.data:                
                # if request.data['inicio'] !='':
                #     filters['created_at__startswith'] = str(request.data['inicio'])
                if request.data['inicio'] and request.data['fin'] !='':
                    filters['created_at__range'] = [str(request.data['inicio']),str(request.data['fin'])]    
          
            #Serializar los datos
            query = FacturasEncabezados.objects.filter(**filters).order_by('-created_at')
            serializer = FacturasListarTablaSerializer(query[offset:limit], many=True)
            new_serializer_data={'cont': query.count(),
            'info':serializer.data}
            #envio de datos
            return Response(new_serializer_data,status=status.HTTP_200_OK)
        except Exception as e: 
            err={"error":'Un error ha ocurrido: {}'.format(e)}  
            createLog(logModel,err,logExcepcion)
            return Response(err, status=status.HTTP_400_BAD_REQUEST) 
#LISTAR TODOS CLIENTE EN ESPECIFICO GRAFICA
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def factura_list_rango_fecha_cliente_grafica(request,pk):
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
            
            query = FacturasEncabezados.objects.raw('''
            SELECT id,YEAR(created_at) anio,MONTH(created_at) mes , COUNT(*) cantidad FROM vittoria_mdm.mdm_facturas_facturasencabezados 
            WHERE  created_at between %s AND %s AND cliente_id = %s AND cliente_id is not null AND state = 1
            GROUP BY MONTH (created_at), YEAR(created_at) ORDER BY MONTH (created_at);''',[str(request.data['inicio']),str(request.data['fin']),pk])
            #Serializar los datos
            data = []
            for raw in query:
                data.append({'anio': raw.anio,'mes': raw.mes,'cantidad': raw.cantidad})
            #envio de datos
            return Response(data,status=status.HTTP_200_OK)
        except Exception as e: 
            err={"error":'Un error ha ocurrido: {}'.format(e)}  
            createLog(logModel,err,logExcepcion)
            return Response(err, status=status.HTTP_400_BAD_REQUEST) 
#LISTAR TODOS CLIENTE EN ESPECIFICO
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def factura_list_rango_fecha_negocio_grafica(request,pk):
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
            
            query = FacturasEncabezados.objects.raw('''
            SELECT id,YEAR(created_at) anio,MONTH(created_at) mes , COUNT(*) cantidad FROM vittoria_mdm.mdm_facturas_facturasencabezados 
            WHERE  created_at between %s AND %s AND negocio_id = %s AND negocio_id is not null AND state = 1
            GROUP BY MONTH (created_at), YEAR(created_at) ORDER BY MONTH (created_at);''',[str(request.data['inicio']),str(request.data['fin']),pk])
            #Serializar los datos
            data = []
            for raw in query:
                data.append({'anio': raw.anio,'mes': raw.mes,'cantidad': raw.cantidad})
            #envio de datos
            return Response(data,status=status.HTTP_200_OK)
        except Exception as e: 
            err={"error":'Un error ha ocurrido: {}'.format(e)}  
            createLog(logModel,err,logExcepcion)
            return Response(err, status=status.HTTP_400_BAD_REQUEST) 
#LISTAR TODOS NEGOCIO EN ESPECIFICO
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def factura_list_rango_fecha_negocio(request,pk):
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
            filters['negocio__isnull'] = False    
            filters['negocio'] = pk    
            if 'inicio' and 'fin' in request.data:                
                # if request.data['inicio'] !='':
                #     filters['created_at__startswith'] = str(request.data['inicio'])
                if request.data['inicio'] and request.data['fin'] !='':
                    filters['created_at__range'] = [str(request.data['inicio']),str(request.data['fin'])]    
          
            #Serializar los datos
            query = FacturasEncabezados.objects.filter(**filters).order_by('-created_at')
            serializer = FacturasListarTablaSerializer(query[offset:limit], many=True)
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
def factura_findOne(request, pk):
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
            query = FacturasEncabezados.objects.get(pk=pk, state=1)
        except FacturasEncabezados.DoesNotExist:
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

#ENCONTRAR LA ULTIMA FACTURA
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def factura_list_latest(request):
    timezone_now = timezone.localtime(timezone.now())
    logModel = {
        'endPoint': logApi+'listLatest/',
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
            filters={"state":"1"}  
            if 'negocio' in request.data:                
                if request.data['negocio'] !='':   
                    filters['negocio__isnull'] = False

            if 'cliente' in request.data:                
                if request.data['cliente'] !='':   
                    filters['cliente__isnull'] = False
            
            query = FacturasEncabezados.objects.filter(**filters).order_by('-id')[0]
        except FacturasEncabezados.DoesNotExist:
            err={"error":"No existe"}  
            createLog(logModel,err,logExcepcion)
            return Response(err,status=status.HTTP_404_NOT_FOUND)
        #tomar el dato
        if request.method == 'GET':
            serializer = FacturasListarSerializer(query)
            createLog(logModel,serializer.data,logTransaccion)
            return Response(serializer.data,status=status.HTTP_200_OK)
    except Exception as e: 
            err={"error":'Un error ha ocurrido: {}'.format(e)}  
            createLog(logModel,err,logExcepcion)
            return Response(err, status=status.HTTP_400_BAD_REQUEST)

#CREAR
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def factura_create(request):
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
            logModel['dataEnviada'] = str(request.data)
            request.data['created_at'] = str(timezone_now)
            if 'updated_at' in request.data:
                request.data.pop('updated_at')

            detalles = request.data['detalles']
            productosSinStock = []
            for detalle in detalles:
                producto = Productos.objects.filter(codigoBarras=detalle['codigo'],state=1).values('stock').first()
                if int(detalle['cantidad']) > int(producto['stock']):
                    productoSinStock={}
                    productoSinStock['codigo']=detalle['codigo']
                    productoSinStock['stock']=producto['stock']
                    productosSinStock.append(productoSinStock)

            if len(productosSinStock) >0:
                return Response(productosSinStock,status=status.HTTP_404_NOT_FOUND)
        
            serializer = FacturaSerializer(data=request.data)
            if serializer.is_valid():                
                serializer.save()
                request.data["factura_id"]= int(serializer.data['id'])
                if serializer.data['negocio'] is None:
                    cliente = Clientes.objects.filter(id=serializer.data['cliente'],state=1).first()
                    request.data["nombres"]= cliente.nombres
                    request.data["apellidos"]= cliente.apellidos
                else:
                    negocio = Negocios.objects.filter(id=serializer.data['negocio'],state=1).first()
                    request.data["nombres"]= negocio.razonSocial
                    request.data["apellidos"]= negocio.nombreComercial

                prediccionCrosselingSerializer = PrediccionCrosselingSerializer(data=request.data)
                prediccionProductosSerializer = PrediccionProductosSerializer(data=request.data)
                prediccionRefilSerializer = PrediccionRefilSerializer(data=request.data)
                if prediccionCrosselingSerializer.is_valid() and prediccionRefilSerializer.is_valid() and prediccionProductosSerializer.is_valid():
                    prediccionCrosselingSerializer.save()
                    prediccionProductosSerializer.save()
                    prediccionRefilSerializer.save()
                    createLog(logModel,serializer.data,logTransaccion)
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                createLog(logModel,serializer.errors,logExcepcion)
                return Response(prediccionCrosselingSerializer.errors, status=status.HTTP_400_BAD_REQUEST)
            createLog(logModel,serializer.errors,logExcepcion)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e: 
            err={"error":'Un error ha ocurrido: {}'.format(e)}  
            createLog(logModel,err,logExcepcion)
            return Response(err, status=status.HTTP_400_BAD_REQUEST)

# ACTUALIZAR
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def factura_update(request, pk):
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
            query = FacturasEncabezados.objects.get(pk=pk, state=1)
            # print(query.detalles.count())
        except FacturasEncabezados.DoesNotExist:
            errorNoExiste={'error':'No existe'}
            createLog(logModel,errorNoExiste,logExcepcion)
            return Response(status=status.HTTP_404_NOT_FOUND)
        if request.method == 'POST':
            now = timezone.localtime(timezone.now())
            request.data['updated_at'] = str(now)
            if 'created_at' in request.data:
                request.data.pop('created_at')
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
def factura_delete(request, pk):
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
            query = FacturasEncabezados.objects.get(pk=pk, state=1)
        except FacturasEncabezados.DoesNotExist:
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
