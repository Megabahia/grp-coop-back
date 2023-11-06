from rest_framework import serializers
# ObjectId
from bson import ObjectId

from ...CORP.corp_empresas.models import Empresas
from ...PERSONAS.personas_personas.models import Personas

from .models import (
    Monedas
)


# NUBE DE coop
# PORTALES: CENTER, PERSONAS, corp, ifis, credit
# Esta clase sirve para conectar el modelo de la tabla de Facturas de la nube de bigpuntos
# para convertir en un objeto de python con el objetivo de manipular los datos y se utiliza
class MonedasSerializer(serializers.ModelSerializer):
    # La clase meta se relaciona con la tabla Monedas
    # el campo fields indica los campos que se devolveran
    # el campo read_only_fields solo permite la lectura
    class Meta:
        model = Monedas
        fields = '__all__'
        read_only_fields = ['_id']

    def create(self, validated_data):
        """
        Este metodo se usa para modificar la respuesta de los campos
        @type instance: El campo instance contiene el registro con los campos
        @rtype: DEvuelve los valores modificados
        """
        monedasUsuario = Monedas.objects.filter(user_id=validated_data['user_id'], state=1).order_by(
            '-created_at').first()
        if monedasUsuario is not None:
            validated_data['saldo'] = validated_data['credito'] + monedasUsuario.saldo
        else:
            validated_data['saldo'] = validated_data['credito']

        monedas = Monedas.objects.create(**validated_data)
        return monedas


# NUBE DE BIGPUNTOS
# PORTALES: CENTER, PERSONAS, corp, ifis, credit
# Esta clase sirve para conectar el modelo de la tabla de Facturas de la nube de bigpuntos
# para convertir en un objeto de python con el objetivo de manipular los datos y se utiliza
class MonedasUsuarioSerializer(serializers.ModelSerializer):
    # La clase meta se relaciona con la tabla Monedas
    # el campo fields indica los campos que se devolveran
    class Meta:
        model = Monedas
        fields = ['saldo']


# NUBE DE coop
# PORTALES: CENTER, PERSONAS, corp, ifis, credit
# Esta clase sirve para conectar el modelo de la tabla de Facturas de la nube de bigpuntos
# para convertir en un objeto de python con el objetivo de manipular los datos y se utiliza
class ListMonedasSerializer(serializers.ModelSerializer):
    # La clase meta se relaciona con la tabla Monedas
    # el campo fields indica los campos que se devolveran
    # el campo read_only_fields solo permite la lectura
    class Meta:
        model = Monedas
        fields = '__all__'
        read_only_fields = ['_id']

    def to_representation(self, instance):
        """
        Este metodo se usa para modificar la respuesta de los campos
        @type instance: El campo instance contiene el registro con los campos
        @rtype: DEvuelve los valores modificados
        """
        data = super(ListMonedasSerializer, self).to_representation(instance)
        empresa_id = data.pop('empresa_id')
        empresa = Empresas.objects.get(pk=ObjectId(empresa_id))
        if empresa:
            data['empresa'] = empresa.nombreEmpresa
        return data


# NUBE DE BIGPUNTOS
# PORTALES: CENTER, PERSONAS, corp, ifis, credit
# Esta clase sirve para conectar el modelo de la tabla de Facturas de la nube de bigpuntos
# para convertir en un objeto de python con el objetivo de manipular los datos y se utiliza
class ListMonedasRegaladasSerializer(serializers.ModelSerializer):
    # La clase meta se relaciona con la tabla Monedas
    # el campo fields indica los campos que se devolveran
    # el campo read_only_fields solo permite la lectura
    class Meta:
        model = Monedas
        fields = '__all__'
        read_only_fields = ['_id']

    def to_representation(self, instance):
        """
        Este metodo se usa para modificar la respuesta de los campos
        @type instance: El campo instance contiene el registro con los campos
        @rtype: DEvuelve los valores modificados
        """
        data = super(ListMonedasRegaladasSerializer, self).to_representation(instance)
        empresa_id = data.pop('empresa_id')
        empresa = Empresas.objects.get(pk=ObjectId(empresa_id))
        if empresa:
            data['empresa'] = empresa.nombreEmpresa
            data['ruc'] = empresa.ruc

        persona = Personas.objects.filter(user_id=instance.user_id, state=1).first()
        if persona:
            data['nombres'] = persona.nombres
            data['apellidos'] = persona.apellidos
            data['identificacion'] = persona.identificacion

        return data


# NUBE DE BIGPUNTOS
# PORTALES: CENTER, PERSONAS, corp, ifis, credit
# Esta clase sirve para conectar el modelo de la tabla de Facturas de la nube de bigpuntos
# para convertir en un objeto de python con el objetivo de manipular los datos y se utiliza
class MonedasGuardarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Monedas
        fields = '__all__'
        read_only_fields = ['_id']
