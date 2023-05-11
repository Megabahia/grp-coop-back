from rest_framework import serializers
from .security import encriptar, desencriptar
import json
from .models import (
    Personas, ValidarCuenta
)


class PersonasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Personas
        fields = '__all__'
        read_only_fields = ['_id']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if representation['identificacion']:
            representation['identificacion'] = desencriptar(eval(representation['identificacion']))
        if representation['nombres']:
            representation['nombres'] = desencriptar(eval(representation['nombres']))
        if representation['apellidos']:
            representation['apellidos'] = desencriptar(eval(representation['apellidos']))
        if representation['nombresCompleto']:
            representation['nombresCompleto'] = desencriptar(eval(representation['nombresCompleto']))
        if representation['genero']:
            representation['genero'] = desencriptar(eval(representation['genero']))
        if representation['fechaNacimiento']:
            representation['fechaNacimiento'] = desencriptar(eval(representation['fechaNacimiento']))
        if representation['edad']:
            representation['edad'] = int(desencriptar(eval(representation['edad'])))
        if representation['ciudad']:
            representation['ciudad'] = desencriptar(eval(representation['ciudad']))
        if representation['provincia']:
            representation['provincia'] = desencriptar(eval(representation['provincia']))
        if representation['pais']:
            representation['pais'] = desencriptar(eval(representation['pais']))
        if representation['direccion']:
            representation['direccion'] = desencriptar(eval(representation['direccion']))

        if representation['telefono']:
            representation['telefono'] = desencriptar(eval(representation['telefono']))
        if representation['whatsapp']:
            representation['whatsapp'] = desencriptar(eval(representation['whatsapp']))

        if representation['empresaInfo']:
            representation['empresaInfo'] = json.loads(desencriptar(eval(representation['empresaInfo'])))
        if representation['datosPyme']:
            representation['datosPyme'] = json.loads(desencriptar(eval(representation['datosPyme'])))
        if representation['estadoCivil']:
            representation['estadoCivil'] = desencriptar(eval(representation['estadoCivil']))
        if representation['cedulaRepresentante']:
            representation['cedulaRepresentante'] = desencriptar(eval(representation['cedulaRepresentante']))
        if representation['direccionRepresentante']:
            representation['direccionRepresentante'] = desencriptar(eval(representation['direccionRepresentante']))
        if representation['celularRepresentante']:
            representation['celularRepresentante'] = desencriptar(eval(representation['celularRepresentante']))
        if representation['whatsappRepresentante']:
            representation['whatsappRepresentante'] = desencriptar(eval(representation['whatsappRepresentante']))
        if representation['correoRepresentante']:
            representation['correoRepresentante'] = desencriptar(eval(representation['correoRepresentante']))
        return representation

    def to_internal_value(self, data):
        if 'identificacion' in data and data.get('identificacion'):
            data['identificacion'] = encriptar(data['identificacion'])
        if 'nombres' in data and data.get('nombres'):
            data['nombres'] = encriptar(data.get('nombres'))
        if 'apellidos' in data and data.get('apellidos'):
            data['apellidos'] = encriptar(data.get('apellidos'))
        if 'nombresCompleto' in data and data.get('nombresCompleto'):
            data['nombresCompleto'] = encriptar(data.get('nombresCompleto'))
        if 'genero' in data and data.get('genero'):
            data['genero'] = encriptar(data.get('genero'))
        if 'fechaNacimiento' in data and data.get('fechaNacimiento'):
            data['fechaNacimiento'] = encriptar(data.get('fechaNacimiento'))
        if 'edad' in data and data.get('edad'):
            data['edad'] = encriptar(str(data.get('edad')))
        if 'ciudad' in data and data.get('ciudad'):
            data['ciudad'] = encriptar(data.get('ciudad'))
        if 'provincia' in data and data.get('provincia'):
            data['provincia'] = encriptar(data.get('provincia'))
        if 'pais' in data and data.get('pais'):
            data['pais'] = encriptar(data.get('pais'))
        if 'direccion' in data and data.get('direccion'):
            data['direccion'] = encriptar(data.get('direccion'))

        if 'telefono' in data and data.get('telefono'):
            data['telefono'] = encriptar(data.get('telefono'))
        if 'whatsapp' in data and data.get('whatsapp'):
            data['whatsapp'] = encriptar(data.get('whatsapp'))

        if 'empresaInfo' in data and data.get('empresaInfo'):
            data['empresaInfo'] = encriptar(json.dumps(data.get('empresaInfo')))
        if 'datosPyme' in data and data.get('datosPyme'):
            data['datosPyme'] = encriptar(json.dumps(data.get('datosPyme')))
        if 'estadoCivil' in data and data.get('estadoCivil'):
            data['estadoCivil'] = encriptar(data.get('estadoCivil'))
        if 'cedulaRepresentante' in data and data.get('cedulaRepresentante'):
            data['cedulaRepresentante'] = encriptar(data.get('cedulaRepresentante'))
        if 'direccionRepresentante' in data and data.get('direccionRepresentante'):
            data['direccionRepresentante'] = encriptar(data.get('direccionRepresentante'))
        if 'celularRepresentante' in data and data.get('celularRepresentante'):
            data['celularRepresentante'] = encriptar(data.get('celularRepresentante'))
        if 'whatsappRepresentante' in data and data.get('whatsappRepresentante'):
            data['whatsappRepresentante'] = encriptar(data.get('whatsappRepresentante'))
        if 'correoRepresentante' in data and data.get('correoRepresentante'):
            data['correoRepresentante'] = encriptar(data.get('correoRepresentante'))
        return data


class PersonasUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Personas
        fields = '__all__'
        read_only_fields = ['user_id']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if representation['identificacion']:
            representation['identificacion'] = desencriptar(eval(representation['identificacion']))
        if representation['nombres']:
            representation['nombres'] = desencriptar(eval(representation['nombres']))
        if representation['apellidos']:
            representation['apellidos'] = desencriptar(eval(representation['apellidos']))
        if representation['nombresCompleto']:
            representation['nombresCompleto'] = desencriptar(eval(representation['nombresCompleto']))
        if representation['genero']:
            representation['genero'] = desencriptar(eval(representation['genero']))
        if representation['fechaNacimiento']:
            representation['fechaNacimiento'] = desencriptar(eval(representation['fechaNacimiento']))
        if representation['edad']:
            representation['edad'] = int(desencriptar(eval(representation['edad'])))
        if representation['ciudad']:
            representation['ciudad'] = desencriptar(eval(representation['ciudad']))
        if representation['provincia']:
            representation['provincia'] = desencriptar(eval(representation['provincia']))
        if representation['pais']:
            representation['pais'] = desencriptar(eval(representation['pais']))
        if representation['direccion']:
            representation['direccion'] = desencriptar(eval(representation['direccion']))

        if representation['telefono']:
            representation['telefono'] = desencriptar(eval(representation['telefono']))
        if representation['whatsapp']:
            representation['whatsapp'] = desencriptar(eval(representation['whatsapp']))

        if representation['empresaInfo']:
            representation['empresaInfo'] = json.loads(desencriptar(eval(representation['empresaInfo'])))
        if representation['datosPyme']:
            representation['datosPyme'] = json.loads(desencriptar(eval(representation['datosPyme'])))
        if representation['estadoCivil']:
            representation['estadoCivil'] = desencriptar(eval(representation['estadoCivil']))
        if representation['cedulaRepresentante']:
            representation['cedulaRepresentante'] = desencriptar(eval(representation['cedulaRepresentante']))
        if representation['direccionRepresentante']:
            representation['direccionRepresentante'] = desencriptar(eval(representation['direccionRepresentante']))
        if representation['celularRepresentante']:
            representation['celularRepresentante'] = desencriptar(eval(representation['celularRepresentante']))
        if representation['whatsappRepresentante']:
            representation['whatsappRepresentante'] = desencriptar(eval(representation['whatsappRepresentante']))
        if representation['correoRepresentante']:
            representation['correoRepresentante'] = desencriptar(eval(representation['correoRepresentante']))
        return representation

    def to_internal_value(self, data):
        if 'identificacion' in data and data.get('identificacion'):
            data['identificacion'] = encriptar(data['identificacion'])
        if 'nombres' in data and data.get('nombres'):
            data['nombres'] = encriptar(data.get('nombres'))
        if 'apellidos' in data and data.get('apellidos'):
            data['apellidos'] = encriptar(data.get('apellidos'))
        if 'nombresCompleto' in data and data.get('nombresCompleto'):
            data['nombresCompleto'] = encriptar(data.get('nombresCompleto'))
        if 'genero' in data and data.get('genero'):
            data['genero'] = encriptar(data.get('genero'))
        if 'fechaNacimiento' in data and data.get('fechaNacimiento'):
            data['fechaNacimiento'] = encriptar(data.get('fechaNacimiento'))
        if 'edad' in data and data.get('edad'):
            data['edad'] = encriptar(str(data.get('edad')))
        if 'ciudad' in data and data.get('ciudad'):
            data['ciudad'] = encriptar(data.get('ciudad'))
        if 'provincia' in data and data.get('provincia'):
            data['provincia'] = encriptar(data.get('provincia'))
        if 'pais' in data and data.get('pais'):
            data['pais'] = encriptar(data.get('pais'))
        if 'direccion' in data and data.get('direccion'):
            data['direccion'] = encriptar(data.get('direccion'))

        if 'telefono' in data and data.get('telefono'):
            data['telefono'] = encriptar(data.get('telefono'))
        if 'whatsapp' in data and data.get('whatsapp'):
            data['whatsapp'] = encriptar(data.get('whatsapp'))

        if 'empresaInfo' in data and data.get('empresaInfo'):
            data['empresaInfo'] = encriptar(json.dumps(data.get('empresaInfo')))
        if 'datosPyme' in data and data.get('datosPyme'):
            data['datosPyme'] = encriptar(json.dumps(data.get('datosPyme')))
        if 'estadoCivil' in data and data.get('estadoCivil'):
            data['estadoCivil'] = encriptar(data.get('estadoCivil'))
        if 'cedulaRepresentante' in data and data.get('cedulaRepresentante'):
            data['cedulaRepresentante'] = encriptar(data.get('cedulaRepresentante'))
        if 'direccionRepresentante' in data and data.get('direccionRepresentante'):
            data['direccionRepresentante'] = encriptar(data.get('direccionRepresentante'))
        if 'celularRepresentante' in data and data.get('celularRepresentante'):
            data['celularRepresentante'] = encriptar(data.get('celularRepresentante'))
        if 'whatsappRepresentante' in data and data.get('whatsappRepresentante'):
            data['whatsappRepresentante'] = encriptar(data.get('whatsappRepresentante'))
        if 'correoRepresentante' in data and data.get('correoRepresentante'):
            data['correoRepresentante'] = encriptar(data.get('correoRepresentante'))
        return data


class PersonasUpdateSinImagenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Personas
        exclude = ['imagen']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if representation['identificacion']:
            representation['identificacion'] = desencriptar(eval(representation['identificacion']))
        if representation['nombres']:
            representation['nombres'] = desencriptar(eval(representation['nombres']))
        if representation['apellidos']:
            representation['apellidos'] = desencriptar(eval(representation['apellidos']))
        if representation['nombresCompleto']:
            representation['nombresCompleto'] = desencriptar(eval(representation['nombresCompleto']))
        if representation['genero']:
            representation['genero'] = desencriptar(eval(representation['genero']))
        if representation['fechaNacimiento']:
            representation['fechaNacimiento'] = desencriptar(eval(representation['fechaNacimiento']))
        if representation['edad']:
            representation['edad'] = int(desencriptar(eval(representation['edad'])))
        if representation['ciudad']:
            representation['ciudad'] = desencriptar(eval(representation['ciudad']))
        if representation['provincia']:
            representation['provincia'] = desencriptar(eval(representation['provincia']))
        if representation['pais']:
            representation['pais'] = desencriptar(eval(representation['pais']))
        if representation['direccion']:
            representation['direccion'] = desencriptar(eval(representation['direccion']))

        if representation['telefono']:
            representation['telefono'] = desencriptar(eval(representation['telefono']))
        if representation['whatsapp']:
            representation['whatsapp'] = desencriptar(eval(representation['whatsapp']))

        if representation['empresaInfo']:
            representation['empresaInfo'] = json.loads(desencriptar(eval(representation['empresaInfo'])))
        if representation['datosPyme']:
            representation['datosPyme'] = json.loads(desencriptar(eval(representation['datosPyme'])))
        if representation['estadoCivil']:
            representation['estadoCivil'] = desencriptar(eval(representation['estadoCivil']))
        if representation['cedulaRepresentante']:
            representation['cedulaRepresentante'] = desencriptar(eval(representation['cedulaRepresentante']))
        if representation['direccionRepresentante']:
            representation['direccionRepresentante'] = desencriptar(eval(representation['direccionRepresentante']))
        if representation['celularRepresentante']:
            representation['celularRepresentante'] = desencriptar(eval(representation['celularRepresentante']))
        if representation['whatsappRepresentante']:
            representation['whatsappRepresentante'] = desencriptar(eval(representation['whatsappRepresentante']))
        if representation['correoRepresentante']:
            representation['correoRepresentante'] = desencriptar(eval(representation['correoRepresentante']))
        return representation

    def to_internal_value(self, data):
        if 'identificacion' in data and data.get('identificacion'):
            data['identificacion'] = encriptar(data['identificacion'])
        if 'nombres' in data and data.get('nombres'):
            data['nombres'] = encriptar(data.get('nombres'))
        if 'apellidos' in data and data.get('apellidos'):
            data['apellidos'] = encriptar(data.get('apellidos'))
        if 'nombresCompleto' in data and data.get('nombresCompleto'):
            data['nombresCompleto'] = encriptar(data.get('nombresCompleto'))
        if 'genero' in data and data.get('genero'):
            data['genero'] = encriptar(data.get('genero'))
        if 'fechaNacimiento' in data and data.get('fechaNacimiento'):
            data['fechaNacimiento'] = encriptar(data.get('fechaNacimiento'))
        if 'edad' in data and data.get('edad'):
            data['edad'] = encriptar(str(data.get('edad')))
        if 'ciudad' in data and data.get('ciudad'):
            data['ciudad'] = encriptar(data.get('ciudad'))
        if 'provincia' in data and data.get('provincia'):
            data['provincia'] = encriptar(data.get('provincia'))
        if 'pais' in data and data.get('pais'):
            data['pais'] = encriptar(data.get('pais'))
        if 'direccion' in data and data.get('direccion'):
            data['direccion'] = encriptar(data.get('direccion'))

        if 'telefono' in data and data.get('telefono'):
            data['telefono'] = encriptar(data.get('telefono'))
        if 'whatsapp' in data and data.get('whatsapp'):
            data['whatsapp'] = encriptar(data.get('whatsapp'))

        if 'empresaInfo' in data and data.get('empresaInfo'):
            data['empresaInfo'] = encriptar(json.dumps(data.get('empresaInfo')))
        if 'datosPyme' in data and data.get('datosPyme'):
            data['datosPyme'] = encriptar(json.dumps(data.get('datosPyme')))
        if 'estadoCivil' in data and data.get('estadoCivil'):
            data['estadoCivil'] = encriptar(data.get('estadoCivil'))
        if 'cedulaRepresentante' in data and data.get('cedulaRepresentante'):
            data['cedulaRepresentante'] = encriptar(data.get('cedulaRepresentante'))
        if 'direccionRepresentante' in data and data.get('direccionRepresentante'):
            data['direccionRepresentante'] = encriptar(data.get('direccionRepresentante'))
        if 'celularRepresentante' in data and data.get('celularRepresentante'):
            data['celularRepresentante'] = encriptar(data.get('celularRepresentante'))
        if 'whatsappRepresentante' in data and data.get('whatsappRepresentante'):
            data['whatsappRepresentante'] = encriptar(data.get('whatsappRepresentante'))
        if 'correoRepresentante' in data and data.get('correoRepresentante'):
            data['correoRepresentante'] = encriptar(data.get('correoRepresentante'))
        return data


class PersonasImagenSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Personas
        fields = ['imagen', 'updated_at']


class ValidarCuentaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ValidarCuenta
        fields = '__all__'
        read_only_fields = ['_id']


class PersonasSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Personas
        fields = ['_id', 'identificacion', 'nombres', 'apellidos', 'user_id', 'whatsapp']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if representation['identificacion']:
            representation['identificacion'] = desencriptar(eval(representation['identificacion']))
        if representation['nombres']:
            representation['nombres'] = desencriptar(eval(representation['nombres']))
        if representation['apellidos']:
            representation['apellidos'] = desencriptar(eval(representation['apellidos']))
        if representation['nombresCompleto']:
            representation['nombresCompleto'] = desencriptar(eval(representation['nombresCompleto']))
        if representation['genero']:
            representation['genero'] = desencriptar(eval(representation['genero']))
        if representation['fechaNacimiento']:
            representation['fechaNacimiento'] = desencriptar(eval(representation['fechaNacimiento']))
        if representation['edad']:
            representation['edad'] = int(desencriptar(eval(representation['edad'])))
        if representation['ciudad']:
            representation['ciudad'] = desencriptar(eval(representation['ciudad']))
        if representation['provincia']:
            representation['provincia'] = desencriptar(eval(representation['provincia']))
        if representation['pais']:
            representation['pais'] = desencriptar(eval(representation['pais']))
        if representation['direccion']:
            representation['direccion'] = desencriptar(eval(representation['direccion']))

        if representation['telefono']:
            representation['telefono'] = desencriptar(eval(representation['telefono']))
        if representation['whatsapp']:
            representation['whatsapp'] = desencriptar(eval(representation['whatsapp']))

        if representation['empresaInfo']:
            representation['empresaInfo'] = json.loads(desencriptar(eval(representation['empresaInfo'])))
        if representation['datosPyme']:
            representation['datosPyme'] = json.loads(desencriptar(eval(representation['datosPyme'])))
        if representation['estadoCivil']:
            representation['estadoCivil'] = desencriptar(eval(representation['estadoCivil']))
        if representation['cedulaRepresentante']:
            representation['cedulaRepresentante'] = desencriptar(eval(representation['cedulaRepresentante']))
        if representation['direccionRepresentante']:
            representation['direccionRepresentante'] = desencriptar(eval(representation['direccionRepresentante']))
        if representation['celularRepresentante']:
            representation['celularRepresentante'] = desencriptar(eval(representation['celularRepresentante']))
        if representation['whatsappRepresentante']:
            representation['whatsappRepresentante'] = desencriptar(eval(representation['whatsappRepresentante']))
        if representation['correoRepresentante']:
            representation['correoRepresentante'] = desencriptar(eval(representation['correoRepresentante']))
        return representation

    def to_internal_value(self, data):
        if 'identificacion' in data and data.get('identificacion'):
            data['identificacion'] = encriptar(data['identificacion'])
        if 'nombres' in data and data.get('nombres'):
            data['nombres'] = encriptar(data.get('nombres'))
        if 'apellidos' in data and data.get('apellidos'):
            data['apellidos'] = encriptar(data.get('apellidos'))
        if 'nombresCompleto' in data and data.get('nombresCompleto'):
            data['nombresCompleto'] = encriptar(data.get('nombresCompleto'))
        if 'genero' in data and data.get('genero'):
            data['genero'] = encriptar(data.get('genero'))
        if 'fechaNacimiento' in data and data.get('fechaNacimiento'):
            data['fechaNacimiento'] = encriptar(data.get('fechaNacimiento'))
        if 'edad' in data and data.get('edad'):
            data['edad'] = encriptar(str(data.get('edad')))
        if 'ciudad' in data and data.get('ciudad'):
            data['ciudad'] = encriptar(data.get('ciudad'))
        if 'provincia' in data and data.get('provincia'):
            data['provincia'] = encriptar(data.get('provincia'))
        if 'pais' in data and data.get('pais'):
            data['pais'] = encriptar(data.get('pais'))
        if 'direccion' in data and data.get('direccion'):
            data['direccion'] = encriptar(data.get('direccion'))

        if 'telefono' in data and data.get('telefono'):
            data['telefono'] = encriptar(data.get('telefono'))
        if 'whatsapp' in data and data.get('whatsapp'):
            data['whatsapp'] = encriptar(data.get('whatsapp'))

        if 'empresaInfo' in data and data.get('empresaInfo'):
            data['empresaInfo'] = encriptar(json.dumps(data.get('empresaInfo')))
        if 'datosPyme' in data and data.get('datosPyme'):
            data['datosPyme'] = encriptar(json.dumps(data.get('datosPyme')))
        if 'estadoCivil' in data and data.get('estadoCivil'):
            data['estadoCivil'] = encriptar(data.get('estadoCivil'))
        if 'cedulaRepresentante' in data and data.get('cedulaRepresentante'):
            data['cedulaRepresentante'] = encriptar(data.get('cedulaRepresentante'))
        if 'direccionRepresentante' in data and data.get('direccionRepresentante'):
            data['direccionRepresentante'] = encriptar(data.get('direccionRepresentante'))
        if 'celularRepresentante' in data and data.get('celularRepresentante'):
            data['celularRepresentante'] = encriptar(data.get('celularRepresentante'))
        if 'whatsappRepresentante' in data and data.get('whatsappRepresentante'):
            data['whatsappRepresentante'] = encriptar(data.get('whatsappRepresentante'))
        if 'correoRepresentante' in data and data.get('correoRepresentante'):
            data['correoRepresentante'] = encriptar(data.get('correoRepresentante'))
        return data
