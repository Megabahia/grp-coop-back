from rest_framework import serializers
# ObjectId
from bson import ObjectId

from apps.CORP.corp_empresas.models import Empresas
from apps.PERSONAS.personas_personas.models import Personas

from apps.CORE.core_monedas.models import (
    Monedas
)


class MonedasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Monedas
        fields = '__all__'
        read_only_fields = ['_id']

    def create(self, validated_data):
        monedasUsuario = Monedas.objects.filter(user_id=validated_data['user_id'], state=1).order_by(
            '-created_at').first()
        if monedasUsuario is not None:
            validated_data['saldo'] = validated_data['credito'] + monedasUsuario.saldo
        else:
            validated_data['saldo'] = validated_data['credito']

        monedas = Monedas.objects.create(**validated_data)
        return monedas


class MonedasUsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Monedas
        fields = ['saldo']


class ListMonedasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Monedas
        fields = '__all__'
        read_only_fields = ['_id']

    def to_representation(self, instance):
        data = super(ListMonedasSerializer, self).to_representation(instance)
        empresa_id = data.pop('empresa_id')
        empresa = Empresas.objects.get(pk=ObjectId(empresa_id))
        if empresa:
            data['empresa'] = empresa.nombreEmpresa
        return data


class ListMonedasRegaladasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Monedas
        fields = '__all__'
        read_only_fields = ['_id']

    def to_representation(self, instance):
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


class MonedasGuardarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Monedas
        fields = '__all__'
        read_only_fields = ['_id']
