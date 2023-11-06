import base64
import requests

from ...CENTRAL.central_catalogo.models import Catalogo
from ...config import config

url = config.API_FIRMA_ELECTRONICO_URL
# Usuario y contraseña para la autenticación básica
usuario = config.API_FIRMA_ELECTRONICO_USERNAME
contrasenia = config.API_FIRMA_ELECTRONICO_PASSWORD

# Codifica las credenciales en base64
credenciales = base64.b64encode(f'{usuario}:{contrasenia}'.encode()).decode()

# Define el encabezado de autorización
encabezado_auth = {'Authorization': f'Basic {credenciales}'}

# LEE ARCHIVO .ENV
import environ

env = environ.Env()
environ.Env.read_env()


def enviarDocumentos(archivos, cliente):
    """
    Este metodo sirve para enviar a firmar los documentos con el proveedor nexty
    @type cliente: recibe los datos del cliente
    @type archivos: recibe los archivos
    @rtype: DEveuele codigo del envio al servicio
    """
    campos = ['_id', 'numeroIdentificacion', 'credito_id', 'created_at', 'updated_at', 'state']
    files = []
    for key, value in archivos.items():
        if key not in campos and value is not None:
            catalogo = Catalogo.objects.filter(tipo='NEXTI', nombre=key).first()
            files.append({
                "filename": value.split('/')[-1],
                "input_path": value,
                "ouput_path": f"{env.str('URL_BUCKET')}CORP/nexti/archivosFirmados/",
                "template_id": '2c995e35651418a37ac7485e' if catalogo is None else catalogo.valor
            })
    # print(cliente)
    data = {
        "data": {
            "product_number": "1020304050",
            "signatory": {
                "client_id": cliente['identificacion'],
                "type": "principal",
                "email": cliente['email'],
                "identification": cliente['identificacion'],
                "phone": "+593" + cliente['celular'],
                "first_name": cliente['nombres'],
                "second_name": cliente['nombres'],
                "first_last_name": cliente['apellidos'],
                "second_last_name": cliente['apellidos'],
                "address": cliente['direccionDomicilio'],
                "postal_code": "170150",
                "state": "Pichincha",
                "city": cliente['ciudad']
            },
            "file_type": "D",
            "files": files
        }
    }

    # Realiza una solicitud GET al endpoint con la autenticación básica
    response = requests.post(url, data, headers=encabezado_auth)
    # Verifica si la solicitud fue exitosa (código de estado 200)
    if response.status_code == 200:
        data = response.text
        print('Respuesta del servidor:', data)
    else:
        print('Error al realizar la solicitud. Código de estado:', response.status_code)
    return response.status_code
