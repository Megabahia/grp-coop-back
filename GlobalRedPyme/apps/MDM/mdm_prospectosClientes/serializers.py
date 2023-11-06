from rest_framework import serializers

from .models import ProspectosClientes


# UTILIZO CREATE, UPDATE, RETRIEVE
class ProspectosClientesSerializer(serializers.ModelSerializer):
    # La clase meta se relaciona con la tabla ProspectosClientes
    # el campo fields indica los campos que se devolveran
    class Meta:
        model = ProspectosClientes
        fields = '__all__'


class ProspectosClientesSearchSerializer(serializers.ModelSerializer):
    # La clase meta se relaciona con la tabla ProspectosClientes
    # el campo fields indica los campos que se devolveran
    class Meta:
        model = ProspectosClientes
        fields = ['id', 'nombres', 'apellidos', 'telefono', 'identificacion', 'whatsapp', 'codigoProducto',
                  'nombreProducto', 'precio']


class ProspectosClientesListarSerializer(serializers.ModelSerializer):
    # La clase meta se relaciona con la tabla ProspectosClientes
    # el campo fields indica los campos que se devolveran
    class Meta:
        model = ProspectosClientes
        fields = ['id', 'nombres', 'apellidos', 'whatsapp', 'correo1', 'correo2', 'ciudad', 'codigoProducto',
                  'created_at']


class ProspectosClienteImagenSerializer(serializers.HyperlinkedModelSerializer):
    # La clase meta se relaciona con la tabla ProspectosClientes
    # el campo fields indica los campos que se devolveran
    class Meta:
        model = ProspectosClientes
        fields = ['imagen', 'updated_at']
