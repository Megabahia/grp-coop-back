from rest_framework import serializers

from .models import Clientes, DatosFisicosClientes, DatosVirtualesClientes, Parientes


class ClientesSerializer(serializers.ModelSerializer):
    # La clase meta se relaciona con la tabla Clientes
    # el campo fields indica los campos que se devolveran
    class Meta:
        model = Clientes
        fields = '__all__'


class ClientesUpdateSerializer(serializers.ModelSerializer):
    # La clase meta se relaciona con la tabla Clientes
    # el campo fields indica los campos que se devolveran
    class Meta:
        model = Clientes
        exclude = ('imagen',)


class ClientesListarSerializer(serializers.ModelSerializer):
    # La clase meta se relaciona con la tabla Clientes
    # el campo fields indica los campos que se devolveran
    class Meta:
        model = Clientes
        fields = ['id', 'nombreCompleto', 'nombres', 'apellidos', 'correo']


class ClienteImagenSerializer(serializers.HyperlinkedModelSerializer):
    # La clase meta se relaciona con la tabla Clientes
    # el campo fields indica los campos que se devolveran
    class Meta:
        model = Clientes
        fields = ['imagen', 'updated_at']


class DatosFisicosClientesSerializer(serializers.ModelSerializer):
    # La clase meta se relaciona con la tabla Clientes
    # el campo fields indica los campos que se devolveran
    class Meta:
        model = DatosFisicosClientes
        fields = '__all__'


class DatosVirtualesClientesSerializer(serializers.ModelSerializer):
    # La clase meta se relaciona con la tabla Clientes
    # el campo fields indica los campos que se devolveran
    class Meta:
        model = DatosVirtualesClientes
        fields = '__all__'


class ParientesSerializer(serializers.ModelSerializer):
    # La clase meta se relaciona con la tabla Clientes
    # el campo fields indica los campos que se devolveran
    class Meta:
        model = Parientes
        fields = '__all__'


class TablaParientesSerializer(serializers.ModelSerializer):
    # La clase meta se relaciona con la tabla Clientes
    # el campo fields indica los campos que se devolveran
    class Meta:
        model = Parientes
        fields = ['id', 'created_at', 'tipoPariente', 'nombres', 'apellidos', 'edad', 'celularPersonal',
                  'correoPersonal']


class ClientePrediccionSerializer(serializers.ModelSerializer):
    # La clase meta se relaciona con la tabla Clientes
    # el campo fields indica los campos que se devolveran
    class Meta:
        model = Clientes
        fields = ['id', 'nombreCompleto', 'correo', 'cedula', 'estado', 'paisNacimiento', 'imagen']
