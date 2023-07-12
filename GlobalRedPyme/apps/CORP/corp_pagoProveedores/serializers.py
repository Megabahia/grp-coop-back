from rest_framework import serializers

from .models import (
    PagoProveedores
)

class PagoProveedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = PagoProveedores
        fields = '__all__'
        read_only_fields = ['_id']

    def to_representation(self, instance):
        data = super(PagoProveedorSerializer, self).to_representation(instance)
        # tomo el campo persona y convierto de OBJECTID a string
        if data['archivoFirmado']:
            data['documentoVerificado'] = prueba_verificar(data['archivoFirmado'].replace('https://globalredpymes.s3.amazonaws.com/', ''))
        else:
            data['documentoVerificado'] = False

        return data



# Importar boto3
import boto3
import tempfile
import environ
from endesive import pdf
def prueba_verificar(url):
    env = environ.Env()
    environ.Env.read_env()  # LEE ARCHIVO .ENV
    client_s3 = boto3.client(
        's3',
        aws_access_key_id=env.str('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=env.str('AWS_SECRET_ACCESS_KEY')
    )
    with tempfile.TemporaryDirectory() as d:
        ruta = d + 'creditosPreAprobados.xlsx'
        s3 = boto3.resource('s3')
        s3.meta.client.download_file('globalredpymes', str(url), ruta)

    try:
        data = open(ruta, "rb").read()
    except:
        print('golaa error')
    no = 0
    for (hashok, signatureok, certok) in pdf.verify(
            data
    ):
        print("*" * 10, "signature no:", no)
        print("signature ok?", signatureok)
        print("hash ok?", hashok)
        print("cert ok?", certok)

    return hashok