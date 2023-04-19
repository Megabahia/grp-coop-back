from rest_framework import serializers

from apps.MDO.mdo_prediccionCrosseling.models import PrediccionCrosseling, Detalles

import requests
import datetime
from apps.config import config

# Listar predicciones crosseling
class PrediccionCrosselingListSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrediccionCrosseling
       	fields = '__all__'

# Guardar Factura
class DetallesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Detalles
       	fields = '__all__'

class PrediccionCrosselingSerializer(serializers.ModelSerializer):
    detalles = DetallesSerializer(many=True)

    class Meta:
        model = PrediccionCrosseling
       	fields = '__all__'

    def create(self, validated_data):
        detalles_data = validated_data.pop('detalles')
        validated_data["fechaPredicciones"] = datetime.datetime.now().date()
        prediccionCrosseling = PrediccionCrosseling.objects.create(**validated_data)
        for detalle_data in detalles_data:
            Detalles.objects.create(prediccionCrosseling=prediccionCrosseling, **detalle_data)
        return prediccionCrosseling

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
class PrediccionCrosselingProductosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Detalles
       	fields = ['id','articulo','codigo','cantidad','precio','informacionAdicional']

    def to_representation(self, instance):
        auth_data = {'codigo': str(instance.codigo)}
        resp = requests.post(config.API_BACK_END+'mdp/productos/prediccionCrosseling/', data=auth_data)
        data = super(PrediccionCrosselingProductosSerializer, self).to_representation(instance)
        
        data['fechaCompra'] = instance.prediccionCrosseling.created_at
        data['predicciones'] = resp.json()

        return data


