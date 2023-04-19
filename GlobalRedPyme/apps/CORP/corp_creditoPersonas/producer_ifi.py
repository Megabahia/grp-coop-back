import boto3
import json
# Importar configuraciones
from ...config import config


def publish(data):
    topicArn = config.AWS_TOPIC_ARN
    snsClient = boto3.client(
        'sns',
        aws_access_key_id=config.AWS_ACCESS_KEY_ID_COLAS,
        aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY_COLAS,
        region_name=config.AWS_REGION_NAME,
    )

    if 'reporteBuro' in data:
        data.pop('reporteBuro')
    if 'identificacion' in data:
        data.pop('identificacion')
    if 'papeletaVotacion' in data:
        data.pop('papeletaVotacion')
    if 'identificacionConyuge' in data:
        data.pop('identificacionConyuge')
    if 'papeletaVotacionConyuge' in data:
        data.pop('papeletaVotacionConyuge')
    if 'planillaLuzNegocio' in data:
        data.pop('planillaLuzNegocio')
    if 'planillaLuzDomicilio' in data:
        data.pop('planillaLuzDomicilio')
    if 'facturas' in data:
        data.pop('facturas')
    if 'matriculaVehiculo' in data:
        data.pop('matriculaVehiculo')
    if 'impuestoPredial' in data:
        data.pop('impuestoPredial')
    if 'buroCredito' in data:
        data.pop('buroCredito')
    if 'evaluacionCrediticia' in data:
        data.pop('evaluacionCrediticia')
    if 'ruc' in data:
        data.pop('ruc')
    if 'rolesPago' in data:
        data.pop('rolesPago')
    if 'panillaIESS' in data:
        data.pop('panillaIESS')
    if 'mecanizadoIess' in data:
        data.pop('mecanizadoIess')
    if 'fotoCarnet' in data:
        data.pop('fotoCarnet')
    if 'solicitudCredito' in data:
        data.pop('solicitudCredito')
    if 'buroCreditoIfis' in data:
        data.pop('buroCreditoIfis')
    if 'documentoAprobacion' in data:
        data.pop('documentoAprobacion')
    if 'pagare' in data:
        data.pop('pagare')
    if 'contratosCuenta' in data:
        data.pop('contratosCuenta')
    if 'tablaAmortizacion' in data:
        data.pop('tablaAmortizacion')
    if 'external_id' in data:
        if data['external_id'] is None:
            data['external_id'] = data['_id']

    response = snsClient.publish(
        TopicArn=topicArn,
        Message=json.dumps(data),
        Subject='PURCHASE',
    )
    print(response['ResponseMetadata']['HTTPStatusCode'])
