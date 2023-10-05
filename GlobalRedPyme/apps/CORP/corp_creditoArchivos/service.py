import base64
import requests
from ...config import config

url = config.API_FIRMA_ELECTRONICO_URL
# Usuario y contraseña para la autenticación básica
usuario = config.API_FIRMA_ELECTRONICO_USERNAME
contrasenia = config.API_FIRMA_ELECTRONICO_PASSWORD

# Codifica las credenciales en base64
credenciales = base64.b64encode(f'{usuario}:{contrasenia}'.encode()).decode()

# Define el encabezado de autorización
encabezado_auth = {'Authorization': f'Basic {credenciales}'}

def enviarDocumentos(archivos, cliente):
    campos = ['_id', 'numeroIdentificacion', 'credito_id', 'created_at', 'updated_at', 'state']
    files = []
    for key, value in archivos.items():
        if key not in campos and value is not None:
            files.append({
                "filename": value.split('/')[-1],
                "url": value,
                "template_id": "1234567890"
            })
    # print(cliente)
    data = {
        "data": {
            "product_number": cliente['identificacion'],
            "ifi_id": archivos['credito_id'],
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
                "city": cliente['ciudad']
            },
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