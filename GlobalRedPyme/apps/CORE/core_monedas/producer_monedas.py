import boto3
import json
# Importar configuraciones
from ...config import config


def publish_monedas_otrogadas(data):
    """
    Este metodo sirve para publicar en la cola de aws
    @type data: El campo data recibe la informacion que se publicara
    @rtype: No devuelve nada
    """
    topicArn = config.AWS_TOPIC_ARN_MONEDAS
    snsClient = boto3.client(
        'sns',
        aws_access_key_id=config.AWS_ACCESS_KEY_ID_COLAS,
        aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY_COLAS,
        region_name=config.AWS_REGION_NAME,
    )
    response = snsClient.publish(
        TopicArn=topicArn,
        Message=json.dumps(data),
        Subject='Credito',
        MessageAttributes={"TransactionType": {"DataType": "String", "StringValue": "PURCHASE"}}
    )
    print('se envio', response['ResponseMetadata']['HTTPStatusCode'])
