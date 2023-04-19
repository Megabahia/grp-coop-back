from rest_framework import serializers

from apps.MDO.mdo_prediccionProductosNuevos.models import PrediccionProductosNuevos, Detalles

import requests
import datetime
from apps.config import config

# Listar predicciones crosseling
class PrediccionProductosListSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrediccionProductosNuevos
       	fields = '__all__'

# Guardar Factura
class DetallesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Detalles
       	fields = '__all__'

class PrediccionProductosSerializer(serializers.ModelSerializer):
    detalles = DetallesSerializer(many=True)

    class Meta:
        model = PrediccionProductosNuevos
       	fields = '__all__'

    def create(self, validated_data):
        detalles_data = validated_data.pop('detalles')
        validated_data["fechaPredicciones"] = datetime.datetime.now().date()
        prediccionProductosNuevos = PrediccionProductosNuevos.objects.create(**validated_data)
        for detalle_data in detalles_data:
            Detalles.objects.create(prediccionProductosNuevos=prediccionProductosNuevos, **detalle_data)
        return prediccionProductosNuevos

# Detalles con imagenes
class DetallesImagenesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Detalles
       	fields = ['id','articulo','codigo','cantidad','precio']

    def to_representation(self, instance):
        auth_data = {'codigo': str(instance.codigo)}
        resp = requests.post(config.API_BACK_END+'mdp/productos/producto/image/', data=auth_data)
        data = super(DetallesImagenesSerializer, self).to_representation(instance)
        if resp.json()['imagen']:
            data['imagen'] = resp.json()['imagen']
        return data

# PREDICCION CROSSELING 
class PrediccionNuevosProductosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Detalles
       	fields = ['id','articulo','codigo','cantidad','precio','informacionAdicional']

    def to_representation(self, instance):
        auth_data = {'producto': str(instance.codigo)}
        resp = requests.post(config.API_BACK_END+'mdp/productos/prediccionProductosNuevos/', data=auth_data)
        data = super(PrediccionNuevosProductosSerializer, self).to_representation(instance)
        
        data['fechaCompra'] = instance.prediccionProductosNuevos.created_at
        data['predicciones'] = resp.json()

        return data


