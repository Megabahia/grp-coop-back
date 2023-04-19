
from apps.CENTRAL.central_acciones.models import Acciones,AccionesPermitidas,AccionesPorRol
from apps.CENTRAL.central_acciones.serializers import AccionesSerializer,AccionesPermitidasSerializer,AccionesPorRolSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
#CRUD ACCIONES
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def acciones_list(request):

    if request.method == 'GET':
        acciones= Acciones.objects.filter(idAccionPadre__isnull=False,state=1)
        serializer = AccionesSerializer(acciones, many=True)
        return Response(serializer.data)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#CREAR
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def acciones_create(request):
    now = timezone.localtime(timezone.now())
    request.data['created_at'] = str(now)
    if 'updated_at' in request.data:
        request.data.pop('updated_at')
    if request.method == 'POST':
        serializer = AccionesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#ENCONTRAR UNO
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def acciones_findOne(request, pk):
    try:
        acciones = Acciones.objects.get(pk=pk, state=1)
    except Acciones.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    #tomar el dato
    if request.method == 'GET':
        serializer = AccionesSerializer(acciones)
        return Response(serializer.data)
   
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#ACTUALIZAR 
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def acciones_update(request, pk):
    try:
        acciones = Acciones.objects.get(pk=pk, state=1)
    except Acciones.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    #tomar el dato
    if request.method == 'POST':
        now = timezone.localtime(timezone.now())
        request.data['updated_at'] = str(now)
        if 'created_at' in request.data:
            request.data.pop('created_at')
        serializer = AccionesSerializer(acciones, data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
   
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#ELIMINAR
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def acciones_delete(request, pk):
    try:
        acciones = Acciones.objects.get(pk=pk, state=1)
    except Acciones.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    #tomar el dato
    if request.method == 'DELETE':
        now = timezone.localtime(timezone.now())
        serializer = AccionesSerializer(acciones, data={'state': '0','updated_at':str(now)},partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
   
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#CRUD ACCIONESPermitidas
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def accionesPermitidas_list(request):

    if request.method == 'GET':
        accionesPermitidas= AccionesPermitidas.objects.filter(state=1)
        serializer = AccionesPermitidasSerializer(accionesPermitidas, many=True)
        return Response(serializer.data)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#CREAR
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def accionesPermitidas_create(request):
    if request.method == 'POST':
        now = timezone.localtime(timezone.now())
        request.data['created_at'] = str(now)
        if 'updated_at' in request.data:
            request.data.pop('updated_at')
        serializer = AccionesPermitidasSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#ENCONTRAR UNO
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def accionesPermitidas_findOne(request, pk):
    try:
        acciones = AccionesPermitidas.objects.get(pk=pk, state=1)
    except AccionesPermitidas.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    #tomar el dato
    if request.method == 'GET':
        serializer = AccionesPermitidasSerializer(accionesPermitidas)
        return Response(serializer.data)
   
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#ACTUALIZAR 
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def accionesPermitidas_update(request, pk):
    try:
        accionesPermitidas = AccionesPermitidas.objects.get(pk=pk, state=1)
    except AccionesPermitidas.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    #tomar el dato
    if request.method == 'POST':
        now = timezone.localtime(timezone.now())
        request.data['updated_at'] = str(now)
        if 'created_at' in request.data:
            request.data.pop('created_at')
        serializer = AccionesPermitidasSerializer(accionesPermitidas, data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
   
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#ELIMINAR
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def accionesPermitidas_delete(request, pk):
    try:
        accionesPermitidas = AccionesPermitidas.objects.get(pk=pk, state=1)
    except AccionesPermitidas.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    #tomar el dato
    if request.method == 'DELETE':
        now = timezone.localtime(timezone.now())
        serializer = AccionesPermitidasSerializer(accionesPermitidas, data={'state': '0','updated_at':str(now)},partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
   
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#CRUD AccionesPorRol
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def accionesPorRol_list(request):

    if request.method == 'GET':
        accionesPorRol= AccionesPorRol.objects.filter(state=1)
        serializer = AccionesPorRolSerializer(accionesPorRol, many=True)
        return Response(serializer.data)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#CREAR
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def accionesPorRol_create(request):
    if request.method == 'POST':
        now = timezone.localtime(timezone.now())
        request.data['created_at'] = str(now)
        if 'updated_at' in request.data:
            request.data.pop('updated_at')
        serializer = AccionesPorRolSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#ENCONTRAR UNO
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def accionesPorRol_findOne(request, pk):
    try:
        acciones = AccionesPorRol.objects.get(pk=pk, state=1)
    except AccionesPorRol.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    #tomar el dato
    if request.method == 'GET':
        serializer = AccionesPorRolSerializer(accionesPorRol)
        return Response(serializer.data)
   
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#ACTUALIZAR 
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def accionesPorRol_update(request, pk):
    try:
        accionesPorRol = AccionesPorRol.objects.get(pk=pk, state=1)
    except AccionesPorRol.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    #tomar el dato
    if request.method == 'POST':
        now = timezone.localtime(timezone.now())
        request.data['updated_at'] = str(now)
        if 'created_at' in request.data:
            request.data.pop('created_at')
        serializer = AccionesPorRolSerializer(accionesPorRol, data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
   
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#ELIMINAR
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def accionesPorRol_delete(request, pk):
    try:
        accionesPorRol = AccionesPorRol.objects.get(pk=pk, state=1)
    except AccionesPorRol.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    #tomar el dato
    if request.method == 'DELETE':
        now = timezone.localtime(timezone.now())
        serializer = AccionesPorRolSerializer(accionesPorRol, data={'state': '0','updated_at':str(now)},partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
   
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
