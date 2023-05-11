from apps.CENTRAL.central_catalogo.models import  Catalogo
from apps.PERSONAS.personas_personas.models import  Personas, ValidarCuenta
from apps.PERSONAS.personas_personas.serializers import (
    PersonasSerializer, PersonasUpdateSerializer, PersonasImagenSerializer, ValidarCuentaSerializer, PersonasUpdateSinImagenSerializer
)
from .security import encriptar
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from django.conf import settings
# Swagger
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
# Generar codigos aleatorios
import string
import random
# TWILIO
from twilio.rest import Client
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
#CREAR
# 'methods' can be used to apply the same modification to multiple methods
@swagger_auto_schema(methods=['post'], request_body=PersonasSerializer)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def personas_create(request):
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
            
            request.data['nombresCompleto'] = request.data['nombres'] +' '+request.data['apellidos']
        
            serializer = PersonasSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                # Genera el codigo
                account_sid = settings.TWILIO_ACCOUNT_SID
                auth_token = settings.TWILIO_AUTH_TOKEN
                client = Client(account_sid, auth_token)
                longitud_codigo = Catalogo.objects.filter(tipo='CONFIG_TWILIO',nombre='LONGITUD_CODIGO',state=1).first().valor
                mensaje = Catalogo.objects.filter(tipo='CONFIG_TWILIO',nombre='MENSAJE',state=1).first().valor
                numeroTwilio = Catalogo.objects.filter(tipo='CONFIG_TWILIO',nombre='NUMERO_TWILIO',state=1).first().valor
                # Genera el codigo
                codigo = (''.join(random.choice(string.digits) for _ in range(int(longitud_codigo))))
                # Guardar codigo en base
                ValidarCuenta.objects.create(codigo=codigo,user_id=request.data['user_id'])
                # Enviar codigo
                message = client.messages.create(
                    from_='whatsapp:'+numeroTwilio,
                    body=mensaje+' '+codigo,
                    to='whatsapp:'+serializer.data['whatsapp']
                )

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
def personas_listOne(request, pk):
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
            query = Personas.objects.filter(user_id=pk, state=1).first()
        except Personas.DoesNotExist:
            err={"error":"No existe"}  
            createLog(logModel,err,logExcepcion)
            return Response(err,status=status.HTTP_404_NOT_FOUND)
        #tomar el dato
        if request.method == 'GET':
            serializer = PersonasSerializer(query)
            createLog(logModel,serializer.data,logTransaccion)
            return Response(serializer.data,status=status.HTTP_200_OK)
    except Exception as e: 
            err={"error":'Un error ha ocurrido: {}'.format(e)}  
            createLog(logModel,err,logExcepcion)
            return Response(err, status=status.HTTP_400_BAD_REQUEST)

# ACTUALIZAR
# 'methods' can be used to apply the same modification to multiple methods
@swagger_auto_schema(methods=['post'], request_body=PersonasSerializer)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def personas_update(request, pk):
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
            query = Personas.objects.filter(user_id=pk, state=1).first()
        except Personas.DoesNotExist:
            errorNoExiste={'error':'No existe'}
            createLog(logModel,errorNoExiste,logExcepcion)
            return Response(status=status.HTTP_404_NOT_FOUND)
        if request.method == 'POST':
            persona = Personas.objects.filter(identificacion=request.data['identificacion'],state=1).first()

            if persona is not None:
                if persona != query:
                    errorNoExiste={'error':'Ya existe otro usuario con la identificacion.'}
                    createLog(logModel,errorNoExiste,logExcepcion)
                    return Response(errorNoExiste,status=status.HTTP_200_OK)

            now = timezone.localtime(timezone.now())
            request.data['updated_at'] = str(now)
            if 'created_at' in request.data:
                request.data.pop('created_at')
            if 'apellidos' in request.data:
                request.data['nombresCompleto'] = request.data['nombres'] +' '+request.data['apellidos']
            serializer = PersonasUpdateSerializer(query, data=request.data,partial=True)
            if serializer.is_valid():
                serializer.save()
                # Genera el codigo
                account_sid = settings.TWILIO_ACCOUNT_SID
                auth_token = settings.TWILIO_AUTH_TOKEN
                client = Client(account_sid, auth_token)
                longitud_codigo = Catalogo.objects.filter(tipo='CONFIG_TWILIO',nombre='LONGITUD_CODIGO',state=1).first().valor
                mensaje = Catalogo.objects.filter(tipo='CONFIG_TWILIO',nombre='MENSAJE',state=1).first().valor
                numeroTwilio = Catalogo.objects.filter(tipo='CONFIG_TWILIO',nombre='NUMERO_TWILIO',state=1).first().valor
                # Genera el codigo
                codigo = (''.join(random.choice(string.digits) for _ in range(int(longitud_codigo))))
                # Guardar codigo en base
                ValidarCuenta.objects.create(codigo=codigo,user_id=request.data['user_id'])
                # Enviar codigo
                # message = client.messages.create(
                #     from_='whatsapp:'+numeroTwilio,
                #     body=mensaje+' '+codigo,
                #     to='whatsapp:'+serializer.data['whatsapp']
                # )

                createLog(logModel,serializer.data,logTransaccion)
                return Response(serializer.data)
            createLog(logModel,serializer.errors,logExcepcion)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e: 
        err={"error":'Un error ha ocurrido: {}'.format(e)}  
        createLog(logModel,err,logExcepcion)
        return Response(err, status=status.HTTP_400_BAD_REQUEST) 

# ACTUALIZAR
# 'methods' can be used to apply the same modification to multiple methods
@swagger_auto_schema(methods=['post'], request_body=PersonasSerializer)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def personas_update_sin_imagen(request, pk):
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
            query = Personas.objects.filter(user_id=pk, state=1).first()
        except Personas.DoesNotExist:
            errorNoExiste={'error':'No existe'}
            createLog(logModel,errorNoExiste,logExcepcion)
            return Response(status=status.HTTP_404_NOT_FOUND)
        if request.method == 'POST':
            now = timezone.localtime(timezone.now())
            request.data['updated_at'] = str(now)
            if 'created_at' in request.data:
                request.data.pop('created_at')
            serializer = PersonasUpdateSinImagenSerializer(query, data=request.data,partial=True)
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
def personas_delete(request, pk):
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
            query = Personas.objects.filter(user_id=pk, state=1).first()
        except Personas.DoesNotExist:
            err={"error":"No existe"}  
            createLog(logModel,err,logExcepcion)
            return Response(err,status=status.HTTP_404_NOT_FOUND)
            return Response(status=status.HTTP_404_NOT_FOUND)
        #tomar el dato
        if request.method == 'DELETE':
            serializer = PersonasSerializer(query, data={'state': '0','updated_at':str(nowDate)},partial=True)
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

# Subir imagen
# 'methods' can be used to apply the same modification to multiple methods
@swagger_auto_schema(methods=['post'], request_body=PersonasImagenSerializer)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def personas_imagenUpdate(request, pk):
    '''id de persona'''
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
            query = Personas.objects.filter(user_id=pk, state=1).first()
        except Personas.DoesNotExist:
            errorNoExiste={'error':'No existe'}
            createLog(logModel,errorNoExiste,logExcepcion)
            return Response(status=status.HTTP_404_NOT_FOUND)
        if request.method == 'POST':
            now = timezone.localtime(timezone.now())
            request.data['updated_at'] = str(now)
            if 'created_at' in request.data:
                request.data.pop('created_at')
            serializer = PersonasImagenSerializer(query, data=request.data,partial=True)
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

# validar codigo
# 'methods' can be used to apply the same modification to multiple methods
@swagger_auto_schema(methods=['post'], request_body=ValidarCuentaSerializer)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def personas_validarCodigo(request):
    nowDate = timezone.localtime(timezone.now())
    timezone_now = timezone.localtime(timezone.now())
    logModel = {
        'endPoint': logApi+'validarCodigo/',
        'modulo':logModulo,
        'tipo' : logExcepcion,
        'accion' : 'ESCRIBIR',
        'fechaInicio' : str(nowDate),
        'dataEnviada' : '{}',
        'fechaFin': str(nowDate),
        'dataRecibida' : '{}'
    }
    try:
        try:
            logModel['dataEnviada'] = str(request.data)
            query = ValidarCuenta.objects.filter(codigo=request.data['codigo'],user_id=request.data['user_id'], state=1).first()
        except ValidarCuenta.DoesNotExist:
            errorNoExiste={'error':'No existe'}
            createLog(logModel,errorNoExiste,logExcepcion)
            return Response(status=status.HTTP_404_NOT_FOUND)
        if request.method == 'POST':
            now = timezone.localtime(timezone.now())
            request.data['updated_at'] = str(now)
            if 'created_at' in request.data:
                request.data.pop('created_at')
            if query is None:
                return Response({"error":"error 400"}, status=status.HTTP_400_BAD_REQUEST)
            serializer = ValidarCuentaSerializer(query, data={'state': '0','updated_at':str(nowDate)},partial=True)
            if serializer.is_valid():
                serializer.save()
                createLog(logModel,serializer.data,logTransaccion)
                return Response({"message":"ok"}, status=status.HTTP_202_ACCEPTED)
            createLog(logModel,serializer.errors,logExcepcion)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e: 
        err={"error":'Un error ha ocurrido: {}'.format(e)}  
        createLog(logModel,err,logExcepcion)
        return Response(err, status=status.HTTP_400_BAD_REQUEST) 


#ENCONTRAR UNO
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def personas_listOne_cedula(request):
    timezone_now = timezone.localtime(timezone.now())
    logModel = {
        'endPoint': logApi+'listOne/cedula/',
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
            hash_resultado = encriptar(request.data['identificacion'])
            query = Personas.objects.filter(identificacion=hash_resultado, state=1).first()
        except Personas.DoesNotExist:
            err={"error":"No existe"}  
            createLog(logModel,err,logExcepcion)
            return Response(err,status=status.HTTP_404_NOT_FOUND)
        #tomar el dato
        if request.method == 'POST':
            serializer = PersonasSerializer(query)
            createLog(logModel,serializer.data,logTransaccion)
            return Response(serializer.data,status=status.HTTP_200_OK)
    except Exception as e: 
            err={"error":'Un error ha ocurrido: {}'.format(e)}  
            createLog(logModel,err,logExcepcion)
            return Response(err, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def personas_update_empresa(request, pk):
    timezone_now = timezone.localtime(timezone.now())
    logModel = {
        'endPoint': logApi+'infoEmpresa/',
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
            query = Personas.objects.filter(user_id=pk, state=1).first()
        except Personas.DoesNotExist:
            errorNoExiste={'error':'No existe'}
            createLog(logModel,errorNoExiste,logExcepcion)
            return Response(status=status.HTTP_404_NOT_FOUND)
        if request.method == 'POST':
            now = timezone.localtime(timezone.now())
            request.data['updated_at'] = str(now)
            if 'created_at' in request.data:
                request.data.pop('created_at')
            serializer = PersonasUpdateSinImagenSerializer(query, data=request.data,partial=True)
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

