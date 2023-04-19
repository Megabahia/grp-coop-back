import io

from django.core.files.uploadedfile import InMemoryUploadedFile
from .models import PagoProveedores
from .serializers import (
    PagoProveedorSerializer
)
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
import json
# Importar boto3
import boto3
import tempfile
import environ
import os
# Import PDF
from fpdf import FPDF
# Enviar Correo
from apps.config.util import sendEmail
# ObjectId
from bson import ObjectId
# logs
from apps.CENTRAL.central_logs.methods import createLog, datosTipoLog, datosProductosMDP

# declaracion variables log
datosAux = datosProductosMDP()
datosTipoLogAux = datosTipoLog()
# asignacion datos modulo
logModulo = datosAux['modulo']
logApi = datosAux['api']
# asignacion tipo de datos
logTransaccion = datosTipoLogAux['transaccion']
logExcepcion = datosTipoLogAux['excepcion']


# CRUD
# CREAR
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def pagoProveedores_create(request):
    request.POST._mutable = True
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

            serializer = PagoProveedorSerializer(data=request.data)
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


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def pagoProveedores_update(request, pk):
    request.POST._mutable = True
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
            query = PagoProveedores.objects.filter(pk=ObjectId(pk), state=1).first()
        except PagoProveedores.DoesNotExist:
            errorNoExiste = {'error': 'No existe'}
            createLog(logModel, errorNoExiste, logExcepcion)
            return Response(status=status.HTTP_404_NOT_FOUND)
        if request.method == 'POST':
            now = timezone.localtime(timezone.now())
            request.data['updated_at'] = str(now)
            if 'created_at' in request.data:
                request.data.pop('created_at')

            if 'claveFirma' in request.data:
                if request.data != '':
                    # certificado = open('/Users/papamacone/Downloads/6194645_identity.p12', 'rb')
                    # pdf2 = open('/Users/papamacone/Downloads/CASH API-v8.pdf', 'rb')
                    datau, datas = firmar(request, query)
                    archivo_pdf_para_enviar_al_cliente = io.BytesIO()
                    archivo_pdf_para_enviar_al_cliente.write(datau)
                    archivo_pdf_para_enviar_al_cliente.write(datas)
                    archivo_pdf_para_enviar_al_cliente.seek(0)

                    request.data['archivoFirmado'] = InMemoryUploadedFile(archivo_pdf_para_enviar_al_cliente,
                                                                          'media',
                                                                          'documentoFirmado.pdf',
                                                                          'application/pdf',
                                                                          archivo_pdf_para_enviar_al_cliente.getbuffer().nbytes,
                                                                          None
                                                                          )

            serializer = PagoProveedorSerializer(query, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                usuario = json.loads(query.usuario)
                if 'Negado' in query.estado:
                    enviarNegadoPago(usuario['email'], query.valorPagar)

                if 'Procesar' in query.estado:
                    enviarProcesandoPago(usuario['email'], query.valorPagar)

                createLog(logModel, serializer.data, logTransaccion)
                return Response(serializer.data)
            createLog(logModel, serializer.errors, logExcepcion)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        err = {"error": 'Un error ha ocurrido: {}'.format(e)}
        createLog(logModel, err, logExcepcion)
        return Response(err, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def pagoProveedores_list(request):
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

            if "empresa_id" in request.data:
                if request.data["empresa_id"] != '':
                    filters['empresa_id'] = str(request.data["empresa_id"])

            # Serializar los datos
            query = PagoProveedores.objects.filter(**filters).order_by('-created_at')
            serializer = PagoProveedorSerializer(query[offset:limit], many=True)
            new_serializer_data = {'cont': query.count(),
                                   'info': serializer.data}
            # envio de datos
            return Response(new_serializer_data, status=status.HTTP_200_OK)
        except Exception as e:
            err = {"error": 'Un error ha ocurrido: {}'.format(e)}
            createLog(logModel, err, logExcepcion)
            return Response(err, status=status.HTTP_400_BAD_REQUEST)

from cryptography.hazmat import backends
from cryptography.hazmat.primitives.serialization import pkcs12
from endesive.pdf import cms

def firmar(request, query):
    usuario = json.loads(query.usuario)
    certificado = request.data['certificado']
    pdf = request.data['pdf']
    contrasenia = request.data['claveFirma']
    date = timezone_now = timezone.localtime(timezone.now())
    date = date.strftime("D:%Y%m%d%H%M%S+00'00'")
    dct = {
        "aligned": 0,
        "sigflags": 3,
        "sigflagsft": 132,
        "sigpage": 0,
        "sigbutton": True,
        "sigfield": "Signature1",
        "auto_sigfield": True,
        "sigandcertify": True,
        "signaturebox": (470, 840, 570, 640),
        "signature": usuario['nombresCompleto'],
        # "signature_img": "signature_test.png",
        "contact": usuario['email'],
        "location": "Ubicación",
        "signingdate": date,
        "reason": "Pago a proveedor " + query.nombrePyme,
        "password": contrasenia,
    }
    # with open("cert.p12", "rb") as fp:
    p12 = pkcs12.load_key_and_certificates(
        certificado.read(), contrasenia.encode("ascii"), backends.default_backend()
    )

    #datau = open(fname, "rb").read()
    datau = pdf.read()
    datas = cms.sign(datau, dct, p12[0], p12[1], p12[2], "sha256")
    return datau, datas
    # return Response('new_serializer_data', status=status.HTTP_200_OK)


def enviarNegadoPago(email, monto):
    subject, from_email, to = 'RAZÓN POR LA QUE SE NIEGA EL PAGO A PROVEEDORES', "08d77fe1da-d09822@inbox.mailtrap.io", \
                              email
    txt_content = f"""
        PAGO A PROVEEDORES - CRÉDITO PAGOS
        
        Lo sentimos!!
        
        La transferencia por ${monto} DE LA FACTURA A PAGAR ha sido rechazada. 
        Por favor revise sus fondos e intente de nuevo.
        
        Si cree que es un error, contáctese con su agente a través de https://walink.co/b5e9c0
        
        Atentamente,
        
        Global RedPyme – Crédito Pagos
    """
    html_content = f"""
                <html>
                    <body>
                        <h1>PAGO A PROVEEDORES - CRÉDITO PAGOS</h1>
                        <br>
                        <h3><b>Lo sentimos!!</b></h3>
                        <br>
                        <p>La transferencia por ${monto} DE LA FACTURA A PAGAR ha sido rechazada. 
                        Por favor revise sus fondos e intente de nuevo.</p>
                        <br>
                        <br>
                        <p>Si cree que es un error, contáctese con su agente a través de https://walink.co/b5e9c0</p>
                        <br>
                        Atentamente,
                        <br>
                        Global RedPyme – Crédito Pagos
                        <br>
                    </body>
                </html>
                """
    sendEmail(subject, txt_content, from_email, to, html_content)


def enviarProcesandoPago(email, monto):
    subject, from_email, to = 'Transferencia exitosa', "08d77fe1da-d09822@inbox.mailtrap.io", \
                              email
    txt_content = f"""
        PAGO A PROVEEDORES - CRÉDITO PAGOS
        
        FELICIDADES!!
        
        La transferencia por ${monto} ha sido realizada con éxito, 
        adjuntamos el comprobante del pago realizado. 
        En 24 horas será acreditado a la cuenta destino.
                            
        Atentamente,
        
        Global RedPyme – Crédito Pagos
    """
    html_content = f"""
                <html>
                    <body>
                        <h1>PAGO A PROVEEDORES - CRÉDITO PAGOS</h1>
                        <br>
                        <h3><b>FELICIDADES!!</b></h3>
                        <br>
                        <p>La transferencia por ${monto} ha sido realizada con éxito, 
                        adjuntamos el comprobante del pago realizado. 
                        En 24 horas será acreditado a la cuenta destino.</p>
                        <br>
                        <br>
                        Atentamente,
                        <br>
                        Global RedPyme – Crédito Pagos
                        <br>
                    </body>
                </html>
                """
    sendEmail(subject, txt_content, from_email, to, html_content)


def generarPDF(datos):
    # save FPDF() class into a
    # variable pdf
    pdf = FPDF()

    # Add a page
    pdf.add_page()

    # set style and size of font
    # that you want in the pdf
    pdf.set_font("Arial", size=15)

    # create a cell
    pdf.cell(200, 10, txt="GeeksforGeeks",
             ln=1, align='C')

    # add another cell
    pdf.cell(200, 10, txt="A Computer Science portal for geeks.",
             ln=2, align='C')

    return pdf