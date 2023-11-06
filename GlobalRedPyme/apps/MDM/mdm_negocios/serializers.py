from rest_framework import serializers

from .models import Negocios, DireccionesEstablecimientosNegocios, PersonalNegocios


# NEGOCIOS
class NegociosSerializer(serializers.ModelSerializer):
    # La clase meta se relaciona con la tabla Negocios
    # el campo fields indica los campos que se devolveran
    class Meta:
        model = Negocios
        fields = '__all__'


# LISTAR NEGOCIOS
class NegociosListarSerializer(serializers.ModelSerializer):
    # La clase meta se relaciona con la tabla Negocios
    # el campo fields indica los campos que se devolveran
    class Meta:
        model = Negocios
        fields = ['id', 'nombreComercial', 'razonSocial', 'imagen']


# SUBIR IMAGEN
class NegociosImagenSerializer(serializers.HyperlinkedModelSerializer):
    # La clase meta se relaciona con la tabla Negocios
    # el campo fields indica los campos que se devolveran
    class Meta:
        model = Negocios
        fields = ['imagen', 'updated_at']


# DIRECCIONES ESTABLECIMIENTOS
class DireccionesEstablecimientosNegociosSerializer(serializers.ModelSerializer):
    # La clase meta se relaciona con la tabla DireccionesEstablecimientosNegocios
    # el campo fields indica los campos que se devolveran
    class Meta:
        model = DireccionesEstablecimientosNegocios
        fields = '__all__'


# PERSONAL NEGOCIOS
class PersonalNegociosSerializer(serializers.ModelSerializer):
    # La clase meta se relaciona con la tabla PersonalNegocios
    # el campo fields indica los campos que se devolveran
    class Meta:
        model = PersonalNegocios
        fields = '__all__'


class NegocioPrediccionSerializer(serializers.ModelSerializer):
    # La clase meta se relaciona con la tabla Negocios
    # el campo fields indica los campos que se devolveran
    class Meta:
        model = Negocios
        fields = ['id', 'nombreComercial', 'correoPersonal', 'ruc', 'estado', 'paisOrigen', 'imagen']
