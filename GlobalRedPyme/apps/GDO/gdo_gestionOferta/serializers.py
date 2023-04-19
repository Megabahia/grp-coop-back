from rest_framework import serializers

from apps.GDO.gdo_gestionOferta.models import Oferta, OfertaDetalles

import requests
from apps.config import config
from django.utils import timezone

# Actualizar factura
class OfertasDetallesSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    class Meta:
        model = OfertaDetalles
       	fields = '__all__'

class OfertasSerializer(serializers.ModelSerializer):
    # id = serializers.IntegerField()
    detalles = OfertasDetallesSerializer(many=True,read_only=True)
    class Meta:
        model = Oferta
       	fields = '__all__'

    def create(self, validated_data):
        detalles_data = validated_data.pop('detalles')
        oferta = Oferta.objects.create(**validated_data)
        for detalle_data in detalles_data:
            OfertaDetalles.objects.create(oferta=oferta, **detalle_data)
        return oferta
    
    def update(self, instance, validated_data):
        # Actualiza la factura cabecera
        instance.__dict__.update(validated_data) 
        instance.save()

        return instance

# Listar las facturas cabecera
class OfertasListarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Oferta
       	fields = '__all__'

# Listar oferta cabecera tabla
class OfertasListarTablaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Oferta
       	fields = ['id','codigo','identificacion','fechaOferta','nombres','apellidos','telefono','correo','indicadorCliente','fechaCompra','comunicoOferta','fechaComunicacion','aceptoOferta','fechaAceptacion','calificacionOferta','vigenciaOferta','canal','total','estado']

# Crear factura
class DetallesSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfertaDetalles
       	fields = '__all__'

class GestionOfertaCreateSerializer(serializers.ModelSerializer):
    detalles = DetallesSerializer(many=True)
    class Meta:
        model = Oferta
       	fields = '__all__'

    def create(self, validated_data):
        detalles_data = validated_data.pop('detalles')
        oferta = Oferta.objects.create(**validated_data)
        for detalle_data in detalles_data:
            OfertaDetalles.objects.create(oferta=oferta, **detalle_data)
        return oferta

# Detalles con imagenes
class DetallesImagenesSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfertaDetalles
       	fields = ['id','producto','codigo','cantidad','precio']

    def to_representation(self, instance):
        auth_data = {'codigo': str(instance.codigo)}
        resp = requests.post(config.API_BACK_END+'mdp/productos/producto/image/', data=auth_data)
        data = super(DetallesImagenesSerializer, self).to_representation(instance)
        if resp.json()['imagen']:
            data['imagen'] = resp.json()['imagen']
        return data