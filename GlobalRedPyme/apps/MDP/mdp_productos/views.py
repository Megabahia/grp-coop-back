from apps.MDP.mdp_productos.models import (
    ProductoImagen,
    Productos, ReporteAbastecimiento, ReporteStock, ReporteCaducidad, ReporteRotacion, IngresoProductos
)
from apps.MDP.mdp_productos.serializers import (
    DetallesSerializer, ProductosActualizarSerializer,
    ProductoCreateSerializer,
    ProductosSerializer, ProductosListSerializer,
    AbastecimientoListSerializer,
    StockListSerializer, CaducidadListSerializer, RotacionListSerializer, RefilListSerializer,
    HistorialAvisosSerializer, ImagenSerializer, PrediccionCrosselingSerializer,
    PrediccionRefilSerializer, PrediccionRefilOneSerializer, ProductoSearchSerializer
)
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from datetime import datetime
#excel
import openpyxl
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
#CRUD PRODUCTOS
#LISTAR TODOS
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def productos_list(request):
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
            if 'empresa_id' in request.data:
                if request.data['empresa_id']!='':
                    filters['empresa_id'] = request.data['empresa_id']

            #Serializar los datos
            query = Productos.objects.filter(**filters).order_by('-created_at')
            serializer = ProductosListSerializer(query[offset:limit], many=True)
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
def productos_findOne(request, pk):
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
            query = Productos.objects.get(pk=pk, state=1)
        except Productos.DoesNotExist:
            err={"error":"No existe"}  
            createLog(logModel,err,logExcepcion)
            return Response(err,status=status.HTTP_404_NOT_FOUND)
        #tomar el dato
        if request.method == 'GET':
            serializer = ProductoCreateSerializer(query)
            createLog(logModel,serializer.data,logTransaccion)
            return Response(serializer.data,status=status.HTTP_200_OK)
    except Exception as e: 
            err={"error":'Un error ha ocurrido: {}'.format(e)}  
            createLog(logModel,err,logExcepcion)
            return Response(err, status=status.HTTP_400_BAD_REQUEST)

# ENCONTRAR IMAGENES
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def producto_images_findOne(request, pk):
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
            query = ProductoImagen.objects.filter(producto=pk, state=1)
        except ProductoImagen.DoesNotExist:
            err={"error":"No existe"}  
            createLog(logModel,err,logExcepcion)
            return Response(err,status=status.HTTP_404_NOT_FOUND)
        #tomar el dato
        if request.method == 'GET':
            serializer = DetallesSerializer(query, many=True)
            createLog(logModel,serializer.data,logTransaccion)
            return Response(serializer.data,status=status.HTTP_200_OK)
    except Exception as e: 
            err={"error":'Un error ha ocurrido: {}'.format(e)}  
            createLog(logModel,err,logExcepcion)
            return Response(err, status=status.HTTP_400_BAD_REQUEST)

# BORRAR IMAGENES
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def producto_images_delete(request, pk):
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
            query = ProductoImagen.objects.get(pk=pk, state=1).delete()
            print(query)
        except ProductoImagen.DoesNotExist:
            err={"error":"No existe"}  
            createLog(logModel,err,logExcepcion)
            return Response(err,status=status.HTTP_404_NOT_FOUND)
        #tomar el dato
        if request.method == 'DELETE':
            data={'message':'Se elimino correctamente.'}            
            if data:
                createLog(logModel,data,logTransaccion)
                return Response(data,status=status.HTTP_200_OK)
            errors={'message':'No se elimino la imagen.'}
            createLog(logModel,errors,logExcepcion)
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e: 
        err={"error":'Un error ha ocurrido: {}'.format(e)}  
        createLog(logModel,err,logExcepcion)
        return Response(err, status=status.HTTP_400_BAD_REQUEST)

#CREAR
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def productos_create(request):
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
        
        logModel['dataEnviada'] = str(request.data)
        query = Productos.objects.filter(codigoBarras=request.data['codigoBarras'], state=1).first()
        if query is not None:
            errorNoExiste={'error':'Ya existe el producto'}
            createLog(logModel,errorNoExiste,logExcepcion)
            return Response(errorNoExiste,status=status.HTTP_404_NOT_FOUND)
        try:
            logModel['dataEnviada'] = str(request.data)
            request.data['created_at'] = str(timezone_now)
            if 'updated_at' in request.data:
                request.data.pop('updated_at')
        
            serializer = ProductoCreateSerializer(data=request.data)
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

# ACTUALIZAR
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def productos_update(request, pk):
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
        logModel['dataEnviada'] = str(request.data)
        query = Productos.objects.filter(codigoBarras=request.data['codigoBarras'], state=1).exclude(pk=pk).first()
        if query is not None:
            errorNoExiste={'error':'Ya existe el producto'}
            createLog(logModel,errorNoExiste,logExcepcion)
            return Response(errorNoExiste,status=status.HTTP_404_NOT_FOUND)
        try:
            logModel['dataEnviada'] = str(request.data)
            query = Productos.objects.get(pk=pk, state=1)
        except Productos.DoesNotExist:
            errorNoExiste={'error':'No existe'}
            createLog(logModel,errorNoExiste,logExcepcion)
            return Response(status=status.HTTP_404_NOT_FOUND)
        if request.method == 'POST':
            now = timezone.localtime(timezone.now())
            request.data['updated_at'] = str(now)
            if 'created_at' in request.data:
                request.data.pop('created_at')
            serializer = ProductosActualizarSerializer(query, data=request.data,partial=True)
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
def productos_delete(request, pk):
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
            query = Productos.objects.get(pk=pk, state=1)
        except Productos.DoesNotExist:
            err={"error":"No existe"}  
            createLog(logModel,err,logExcepcion)
            return Response(err,status=status.HTTP_404_NOT_FOUND)
            return Response(status=status.HTTP_404_NOT_FOUND)
        #tomar el dato
        if request.method == 'DELETE':
            serializer = ProductosSerializer(query, data={'state': '0','updated_at':str(nowDate)},partial=True)
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

# SEARCH PRODUCTO
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def search_producto_list(request):
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
            if 'codigoBarras' in request.data:
                if request.data['codigoBarras']!='':
                    filters['codigoBarras__icontains'] = str(request.data['codigoBarras'])
            if 'nombre' in request.data:
                if request.data['nombre']!='':
                    filters['nombre__icontains'] = str(request.data['nombre'])
          
            #Serializar los datos
            query = Productos.objects.filter(**filters).order_by('-created_at')
            serializer = ProductosListSerializer(query[offset:limit], many=True)
            new_serializer_data={'cont': query.count(),
            'info':serializer.data}
            #envio de datos
            return Response(new_serializer_data,status=status.HTTP_200_OK)
        except Exception as e: 
            err={"error":'Un error ha ocurrido: {}'.format(e)}  
            createLog(logModel,err,logExcepcion)
            return Response(err, status=status.HTTP_400_BAD_REQUEST) 

# SEARCH PRODUCTO
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def search_producto_codigo_list(request):
    timezone_now = timezone.localtime(timezone.now())
    logModel = {
        'endPoint': logApi+'search/producto/codigo/',
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
            query = Productos.objects.filter(codigoBarras=request.data['codigoBarras'], state=1).first()
        except Productos.DoesNotExist:
            err={"error":"No existe"}  
            createLog(logModel,err,logExcepcion)
            return Response(err,status=status.HTTP_404_NOT_FOUND)
        #tomar el dato
        if request.method == 'POST':
            serializer = ProductoSearchSerializer(query)
            createLog(logModel,serializer.data,logTransaccion)
            return Response(serializer.data,status=status.HTTP_200_OK)
    except Exception as e: 
            err={"error":'Un error ha ocurrido: {}'.format(e)}  
            createLog(logModel,err,logExcepcion)
            return Response(err, status=status.HTTP_400_BAD_REQUEST)

# ABASTECIMIENTO
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def abastecimiento_list(request):
    timezone_now = timezone.localtime(timezone.now())
    logModel = {
        'endPoint': logApi+'abastecimiento/list/',
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
            if request.data['inicio']!='':
                filters['fechaMaximaStock__gte'] = str(request.data['inicio'])   
            if request.data['fin']!='':
                filters['fechaMaximaStock__lte'] = str(request.data['fin'])              
            if 'categoria' in request.data:
                if request.data['categoria']!='':
                    filters['producto__categoria__icontains'] = str(request.data['categoria'])                    
            if 'subCategoria' in request.data:
                if request.data['subCategoria']!='':
                    filters['producto__subCategoria__icontains'] = str(request.data['subCategoria'])                    
            if 'empresa_id' in request.data:
                if request.data['empresa_id']!='':
                    filters['empresa_id'] = request.data['empresa_id']

            #Serializar los datos
            query = ReporteAbastecimiento.objects.filter(**filters).order_by('-created_at')
            serializer = AbastecimientoListSerializer(query[offset:limit], many=True)
            new_serializer_data={'cont': query.count(),
            'info':serializer.data}
            #envio de datos
            return Response(new_serializer_data,status=status.HTTP_200_OK)
        except Exception as e: 
            err={"error":'Un error ha ocurrido: {}'.format(e)}  
            createLog(logModel,err,logExcepcion)
            return Response(err, status=status.HTTP_400_BAD_REQUEST)

# STOCK
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def stock_list(request):
    timezone_now = timezone.localtime(timezone.now())
    logModel = {
        'endPoint': logApi+'caducidad/list/',
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
            if request.data['inicio']!='':
                filters['fechaUltimaStock__gte'] = str(request.data['inicio'])   
            if request.data['fin']!='':
                filters['fechaUltimaStock__lte'] = str(request.data['fin'])              
            if 'categoria' in request.data:
                if request.data['categoria']!='':
                    filters['producto__categoria__icontains'] = str(request.data['categoria'])                    
            if 'subCategoria' in request.data:
                if request.data['subCategoria']!='':
                    filters['producto__subCategoria__icontains'] = str(request.data['subCategoria'])                    
            if 'empresa_id' in request.data:
                if request.data['empresa_id']!='':
                    filters['empresa_id'] = request.data['empresa_id']

            #Serializar los datos
            query = ReporteStock.objects.filter(**filters).order_by('-created_at')
            serializer = StockListSerializer(query[offset:limit], many=True)
            new_serializer_data={'cont': query.count(),
            'info':serializer.data}
            #envio de datos
            return Response(new_serializer_data,status=status.HTTP_200_OK)
        except Exception as e: 
            err={"error":'Un error ha ocurrido: {}'.format(e)}  
            createLog(logModel,err,logExcepcion)
            return Response(err, status=status.HTTP_400_BAD_REQUEST)

# CADUCIDAD
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def caducidad_list(request):
    timezone_now = timezone.localtime(timezone.now())
    logModel = {
        'endPoint': logApi+'caducidad/list/',
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
            if request.data['inicio']!='':
                filters['fechaCaducidad__gte'] = str(request.data['inicio'])   
            if request.data['fin']!='':
                filters['fechaCaducidad__lte'] = str(request.data['fin'])              
            if 'categoria' in request.data:
                if request.data['categoria']!='':
                    filters['producto__categoria__icontains'] = str(request.data['categoria'])                    
            if 'subCategoria' in request.data:
                if request.data['subCategoria']!='':
                    filters['producto__subCategoria__icontains'] = str(request.data['subCategoria'])                    
            if 'empresa_id' in request.data:
                if request.data['empresa_id']!='':
                    filters['empresa_id'] = request.data['empresa_id']

            #Serializar los datos
            query = ReporteCaducidad.objects.filter(**filters).order_by('-created_at')
            serializer = CaducidadListSerializer(query[offset:limit], many=True)
            new_serializer_data={'cont': query.count(),
            'info':serializer.data}
            #envio de datos
            return Response(new_serializer_data,status=status.HTTP_200_OK)
        except Exception as e: 
            err={"error":'Un error ha ocurrido: {}'.format(e)}  
            createLog(logModel,err,logExcepcion)
            return Response(err, status=status.HTTP_400_BAD_REQUEST)

# ROTACION
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def rotacion_list(request):
    timezone_now = timezone.localtime(timezone.now())
    logModel = {
        'endPoint': logApi+'rotacion/list/',
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
            if request.data['inicio']!='':
                filters['fechaInicio__gte'] = str(request.data['inicio'])   
            if request.data['fin']!='':
                filters['fechaFin__lte'] = str(request.data['fin'])              
            if 'categoria' in request.data:
                if request.data['categoria']!='':
                    filters['producto__categoria__icontains'] = str(request.data['categoria'])                    
            if 'subCategoria' in request.data:
                if request.data['subCategoria']!='':
                    filters['producto__subCategoria__icontains'] = str(request.data['subCategoria'])                    
            if 'empresa_id' in request.data:
                if request.data['empresa_id']!='':
                    filters['empresa_id'] = request.data['empresa_id']

            #Serializar los datos
            query = ReporteRotacion.objects.filter(**filters).order_by('-created_at')
            serializer = RotacionListSerializer(query[offset:limit], many=True)
            new_serializer_data={'cont': query.count(),
            'info':serializer.data}
            #envio de datos
            return Response(new_serializer_data,status=status.HTTP_200_OK)
        except Exception as e: 
            err={"error":'Un error ha ocurrido: {}'.format(e)}  
            createLog(logModel,err,logExcepcion)
            return Response(err, status=status.HTTP_400_BAD_REQUEST) 

# REFIL
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def refil_list(request):
    timezone_now = timezone.localtime(timezone.now())
    logModel = {
        'endPoint': logApi+'refil/list/',
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
            if request.data['inicio']!='' and request.data['fin'] != '':
                filters['refil__range'] = [int(request.data['inicio']), int(request.data['fin'])]
            elif request.data['inicio']!='':
                filters['refil__gte'] = str(request.data['inicio'])   
            elif request.data['fin']!='':
                filters['refil__lte'] = str(request.data['fin'])              
            if 'categoria' in request.data:
                if request.data['categoria']!='':
                    filters['categoria__icontains'] = str(request.data['categoria'])                    
            if 'subCategoria' in request.data:
                if request.data['subCategoria']!='':
                    filters['subCategoria__icontains'] = str(request.data['subCategoria'])                    
            if 'empresa_id' in request.data:
                if request.data['empresa_id']!='':
                    filters['empresa_id'] = request.data['empresa_id']

            #Serializar los datos
            query = Productos.objects.filter(**filters).order_by('-created_at')
            serializer = RefilListSerializer(query[offset:limit], many=True)
            new_serializer_data={'cont': query.count(),
            'info':serializer.data}
            #envio de datos
            return Response(new_serializer_data,status=status.HTTP_200_OK)
        except Exception as e: 
            err={"error":'Un error ha ocurrido: {}'.format(e)}  
            createLog(logModel,err,logExcepcion)
            return Response(err, status=status.HTTP_400_BAD_REQUEST) 

# METODO SUBIR ARCHIVOS EXCEL
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def uploadEXCEL_crearProductos(request):
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
            worksheet = wb["Hoja1"]
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
                if worksheet.iter_cols():
                    resultadoInsertar=insertarDato_Producto(dato)
                    if resultadoInsertar!='Dato insertado correctamente':
                        if resultadoInsertar in 'Codigo producto':
                            contInvalidos+=1 
                            errores.append({"error":"Producto no encontrado "+str(contTotal)+": "+str(resultadoInsertar)})
                        else:
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

# INSERTAR DATOS EN LA BASE INDIVIDUAL
def insertarDato_Producto(dato):
    try:
        timezone_now = timezone.localtime(timezone.now())
        data={}
        data['codigoBarras'] = dato[0].replace('"', "") if dato[0].replace('"', "") != "NULL" else None
        data['descripcion'] = dato[1].replace('"', "") if dato[1] != "NULL" else None
        data['stock'] = dato[2].replace('"', "") if dato[2] != "NULL" else None        
        data['lote'] = dato[3].replace('"', "") if dato[3] != "NULL" else None
        data['fechaElaboracion'] = str(dato[4].replace('"', "")[:10]) if dato[4] != "NULL" else None   
        data['fechaCaducidad'] = str(dato[5].replace('"', "")[:10]) if dato[5] != "NULL" else None
        data['costoCompra'] = str(dato[6].replace('"', "")) if dato[6] != "NULL" else None
        data['updated_at'] = str(timezone_now)
        #inserto el dato con los campos requeridos
        query = Productos.objects.get(codigoBarras=data['codigoBarras'])
        for key, value in data.items():
            setattr(query, key, value)
        query.save()
        if query == 0:
            return 'Codigo producto %(code)s no existe' % {"code": data['codigoBarras']}
        # CREAR INGRESO PRODUCTOS
        IngresoProductos.objects.create(cantidad = data['stock'], fechaElaboracion = str(data['fechaElaboracion']), fechaCaducidad = str(data['fechaCaducidad']), precioCompra = data['costoCompra'], producto = query)
        # CREAR REPORTE STOCK
        ReporteStock.objects.create(fechaUltimaStock = datetime.today().strftime('%Y-%m-%d'), montoCompra = data['costoCompra'], producto = query)
        return 'Dato insertado correctamente'
    except Exception as e:
        return str(e)

#CREAR ABASTECIMIENTO
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def abastecimiento_create(request):
    timezone_now = timezone.localtime(timezone.now())
    logModel = {
        'endPoint': logApi+'abastecimiento/create/',
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
            # request.data['created_at'] = str(timezone_now)
            # if 'updated_at' in request.data:
            #     request.data.pop('updated_at')

            serializer = HistorialAvisosSerializer(data=request.data['data'], many=True)
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

# OBTENER URL IMAGEN
@api_view(['POST'])
def productoImagen_list(request):
    timezone_now = timezone.localtime(timezone.now())
    logModel = {
        'endPoint': logApi+'producto/image/',
        'modulo':logModulo,
        'tipo' : logExcepcion,
        'accion' : 'CREAR',
        'fechaInicio' : str(timezone_now),
        'dataEnviada' : '{}',
        'fechaFin': str(timezone_now),
        'dataRecibida' : '{}'
    }
    try:
        try:
            query = ProductoImagen.objects.filter(producto__codigoBarras=str(request.data['codigo']), producto__state=1).first()            
        except ProductoImagen.DoesNotExist:
            err={"error":"No existe"}  
            createLog(logModel,err,logExcepcion)
            return Response(err,status=status.HTTP_404_NOT_FOUND)
        #tomar el dato
        if request.method == 'POST':
            serializer = ImagenSerializer(query)
            createLog(logModel,serializer.data,logTransaccion)
            return Response(serializer.data,status=status.HTTP_200_OK)
    except Exception as e: 
            err={"error":'Un error ha ocurrido: {}'.format(e)}  
            createLog(logModel,err,logExcepcion)
            return Response(err, status=status.HTTP_400_BAD_REQUEST)

# OBTENER PREDICCION CROSSELING
@api_view(['POST'])
def prediccion_crosseling_list(request):
    timezone_now = timezone.localtime(timezone.now())
    logModel = {
        'endPoint': logApi+'prediccionCrosseling/',
        'modulo':logModulo,
        'tipo' : logExcepcion,
        'accion' : 'CREAR',
        'fechaInicio' : str(timezone_now),
        'dataEnviada' : '{}',
        'fechaFin': str(timezone_now),
        'dataRecibida' : '{}'
    }
    try:
        try:                 
            query = Productos.objects.filter(codigoBarras=str(request.data['codigo']), state=1).first()   
        except Productos.DoesNotExist:
            err={"error":"No existe"}  
            createLog(logModel,err,logExcepcion)
            return Response(err,status=status.HTTP_404_NOT_FOUND)
        #tomar el dato
        if request.method == 'POST':
            query = ReporteRotacion.objects.filter(producto__subCategoria = query.subCategoria,tipoRotacion = 'Bajo',state = 1).order_by('-created_at','-producto__stock')
            serializer = PrediccionCrosselingSerializer(query[0:3], many = True)
            createLog(logModel,serializer.data,logTransaccion)
            return Response(serializer.data,status=status.HTTP_200_OK)
    except Exception as e: 
            err={"error":'Un error ha ocurrido: {}'.format(e)}  
            createLog(logModel,err,logExcepcion)
            return Response(err, status=status.HTTP_400_BAD_REQUEST)

# OBTENER PRODUCTO REFIL
@api_view(['POST'])
def producto_refil_list(request):
    timezone_now = timezone.localtime(timezone.now())
    logModel = {
        'endPoint': logApi+'prediccionCrosseling/',
        'modulo':logModulo,
        'tipo' : logExcepcion,
        'accion' : 'CREAR',
        'fechaInicio' : str(timezone_now),
        'dataEnviada' : '{}',
        'fechaFin': str(timezone_now),
        'dataRecibida' : '{}'
    }
    try:
        try:                 
            query = Productos.objects.filter(codigoBarras=request.data['producto'], state=1)
        except Productos.DoesNotExist:
            err={"error":"No existe"}  
            createLog(logModel,err,logExcepcion)
            return Response(err,status=status.HTTP_404_NOT_FOUND)
        #tomar el dato
        if request.method == 'POST':            
            serializer = PrediccionRefilSerializer(query, many = True)
            createLog(logModel,serializer.data,logTransaccion)
            return Response(serializer.data,status=status.HTTP_200_OK)
    except Exception as e: 
            err={"error":'Un error ha ocurrido: {}'.format(e)}  
            createLog(logModel,err,logExcepcion)
            return Response(err, status=status.HTTP_400_BAD_REQUEST)

# OBTENER PREDICCION REFIL
@api_view(['POST'])
def prediccion_refil_list(request):
    timezone_now = timezone.localtime(timezone.now())
    logModel = {
        'endPoint': logApi+'prediccionRefil/',
        'modulo':logModulo,
        'tipo' : logExcepcion,
        'accion' : 'CREAR',
        'fechaInicio' : str(timezone_now),
        'dataEnviada' : '{}',
        'fechaFin': str(timezone_now),
        'dataRecibida' : '{}'
    }
    try:
        try:                 
            query = ProductoImagen.objects.filter(producto__codigoBarras=request.data['producto'], state=1).first()      
        except ProductoImagen.DoesNotExist:
            err={"error":"No existe"}  
            createLog(logModel,err,logExcepcion)
            return Response(err,status=status.HTTP_404_NOT_FOUND)
        #tomar el dato
        if request.method == 'POST':
            serializer = PrediccionRefilOneSerializer(query)
            createLog(logModel,serializer.data,logTransaccion)
            return Response(serializer.data,status=status.HTTP_200_OK)
    except Exception as e: 
            err={"error":'Un error ha ocurrido: {}'.format(e)}  
            createLog(logModel,err,logExcepcion)
            return Response(err, status=status.HTTP_400_BAD_REQUEST)

# OBTENER PREDICCION PRODUCTOS NUEVOS
@api_view(['POST'])
def prediccion_productosNuevos_list(request):
    timezone_now = timezone.localtime(timezone.now())
    logModel = {
        'endPoint': logApi+'prediccionProductosNuevos/',
        'modulo':logModulo,
        'tipo' : logExcepcion,
        'accion' : 'CREAR',
        'fechaInicio' : str(timezone_now),
        'dataEnviada' : '{}',
        'fechaFin': str(timezone_now),
        'dataRecibida' : '{}'
    }
    try:
        try:                 
            query = ProductoImagen.objects.filter(producto__codigoBarras=request.data['producto'], state=1).first()
        except ProductoImagen.DoesNotExist:
            err={"error":"No existe"}  
            createLog(logModel,err,logExcepcion)
            return Response(err,status=status.HTTP_404_NOT_FOUND)
        #tomar el dato
        if request.method == 'POST':
            
            query = ReporteRotacion.objects.filter(producto__categoria = query.producto.categoria,tipoRotacion = 'Bajo',state = 1).order_by('-created_at','-producto__stock')
            serializer = PrediccionCrosselingSerializer(query[0:3], many = True)
            createLog(logModel,serializer.data,logTransaccion)
            return Response(serializer.data,status=status.HTTP_200_OK)
    except Exception as e: 
            err={"error":'Un error ha ocurrido: {}'.format(e)}  
            createLog(logModel,err,logExcepcion)
            return Response(err, status=status.HTTP_400_BAD_REQUEST)

