from rest_framework import serializers

from .models import PrediccionRefil, Detalles

import requests
import datetime
from apps.config import config


# Listar predicciones crosseling
class PrediccionRefilListSerializer(serializers.ModelSerializer):
    # La clase meta se relaciona con la tabla Facturas
    # el campo fields indica los campos que se devolveran
    class Meta:
        model = PrediccionRefil
        fields = '__all__'


# Guardar Factura
class DetallesSerializer(serializers.ModelSerializer):
    # La clase meta se relaciona con la tabla Facturas
    # el campo fields indica los campos que se devolveran
    class Meta:
        model = Detalles
        fields = '__all__'


class PrediccionRefilSerializer(serializers.ModelSerializer):
    detalles = DetallesSerializer(many=True)

    # La clase meta se relaciona con la tabla Facturas
    # el campo fields indica los campos que se devolveran
    class Meta:
        model = PrediccionRefil
        fields = '__all__'

    def create(self, validated_data):
        """
        Este metodo sirve para crear la prediccion en la tabla predicciones de la base datos mdo
        @type validated_data: El campo validated_data recibe los campos para ingresar en la prediccion
        @rtype: Devuelve el registro creado
        """
        detalles_data = validated_data.pop('detalles')
        validated_data["fechaPredicciones"] = datetime.datetime.now().date()
        if 'cliente' in validated_data:
            prediccionRefil = PrediccionRefil.objects.filter(fechaPredicciones=validated_data['fechaPredicciones'],
                                                             cliente=validated_data['cliente'], state=1).first()
            if prediccionRefil is None:
                prediccionRefil = PrediccionRefil.objects.create(**validated_data)
        else:
            prediccionRefil = PrediccionRefil.objects.filter(fechaPredicciones=validated_data['fechaPredicciones'],
                                                             negocio=validated_data['negocio'], state=1).first()
            if prediccionRefil is None:
                prediccionRefil = PrediccionRefil.objects.create(**validated_data)

        for detalle_data in detalles_data:
            Detalles.objects.create(prediccionRefil=prediccionRefil, **detalle_data)
        return prediccionRefil


# Detalles con imagenes
class DetallesImagenesSerializer(serializers.ModelSerializer):
    # La clase meta se relaciona con la tabla Facturas
    # el campo fields indica los campos que se devolveran
    class Meta:
        model = Detalles
        fields = ['id', 'articulo', 'codigo', 'cantidad', 'precio']

    def to_representation(self, instance):
        """
        Este metodo se usa para modificar la respuesta de los campos
        @type instance: El campo instance contiene el registro con los campos
        @rtype: DEvuelve los valores modificados
        """
        auth_data = {'codigo': str(instance.codigo)}
        resp = requests.post(config.API_BACK_END + 'mdp/productos/producto/image/', data=auth_data)
        data = super(DetallesImagenesSerializer, self).to_representation(instance)
        if resp.json()['imagen']:
            data['imagen'] = resp.json()['imagen']
        return data


# PREDICCION Refil
class PrediccionRefilProductosSerializer(serializers.ModelSerializer):
    # La clase meta se relaciona con la tabla Facturas
    # el campo fields indica los campos que se devolveran
    class Meta:
        model = Detalles
        fields = ['id', 'articulo', 'codigo', 'cantidad', 'precio', 'informacionAdicional']

    def to_representation(self, instance):
        """
        Este metodo se usa para modificar la respuesta de los campos
        @type instance: El campo instance contiene el registro con los campos
        @rtype: DEvuelve los valores modificados
        """
        auth_data = {'producto': str(instance.codigo)}
        resp = requests.post(config.API_BACK_END + 'mdp/productos/prediccionRefil/', data=auth_data)
        data = super(PrediccionRefilProductosSerializer, self).to_representation(instance)

        data['fechaCompra'] = instance.prediccionRefil.created_at
        data['predicciones'] = resp.json()

        return data
