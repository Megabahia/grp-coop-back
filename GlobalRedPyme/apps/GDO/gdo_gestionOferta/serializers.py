from rest_framework import serializers

from .models import Oferta, OfertaDetalles

import requests
from ...config import config


# Actualizar factura
class OfertasDetallesSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    # La clase meta se relaciona con la tabla OfertaDetalles
    # el campo fields indica los campos que se devolveran
    class Meta:
        model = OfertaDetalles
        fields = '__all__'


class OfertasSerializer(serializers.ModelSerializer):
    # id = serializers.IntegerField()
    detalles = OfertasDetallesSerializer(many=True, read_only=True)

    # La clase meta se relaciona con la tabla OfertaDetalles
    # el campo fields indica los campos que se devolveran
    class Meta:
        model = Oferta
        fields = '__all__'

    def create(self, validated_data):
        """
        Este metodo sirve para crear la oferta
        @type validated_data: El campo validated_data recibe los campos de la tabla oferta
        @rtype: Devuelve la ofreta creada
        """
        detalles_data = validated_data.pop('detalles')
        oferta = Oferta.objects.create(**validated_data)
        for detalle_data in detalles_data:
            OfertaDetalles.objects.create(oferta=oferta, **detalle_data)
        return oferta

    def update(self, instance, validated_data):
        """
        Este metodo sirve para crear la oferta
        @type instance: El campo instance recibe los valores de la tabla oferta
        @type validated_data: El campo validated_data recibe los campos de la tabla oferta
        @rtype: Devuelve la ofreta creada
        """
        # Actualiza la factura cabecera
        instance.__dict__.update(validated_data)
        instance.save()

        return instance


# Listar las facturas cabecera
class OfertasListarSerializer(serializers.ModelSerializer):
    # La clase meta se relaciona con la tabla Oferta
    # el campo fields indica los campos que se devolveran
    class Meta:
        model = Oferta
        fields = '__all__'


# Listar oferta cabecera tabla
class OfertasListarTablaSerializer(serializers.ModelSerializer):
    # La clase meta se relaciona con la tabla Oferta
    # el campo fields indica los campos que se devolveran
    class Meta:
        model = Oferta
        fields = ['id', 'codigo', 'identificacion', 'fechaOferta', 'nombres', 'apellidos', 'telefono', 'correo',
                  'indicadorCliente', 'fechaCompra', 'comunicoOferta', 'fechaComunicacion', 'aceptoOferta',
                  'fechaAceptacion', 'calificacionOferta', 'vigenciaOferta', 'canal', 'total', 'estado']


# Crear factura
class DetallesSerializer(serializers.ModelSerializer):
    # La clase meta se relaciona con la tabla OfertaDetalles
    # el campo fields indica los campos que se devolveran
    class Meta:
        model = OfertaDetalles
        fields = '__all__'


class GestionOfertaCreateSerializer(serializers.ModelSerializer):
    detalles = DetallesSerializer(many=True)

    # La clase meta se relaciona con la tabla Publicaciones
    # el campo fields indica los campos que se devolveran
    class Meta:
        model = Oferta
        fields = '__all__'

    def create(self, validated_data):
        """
        Este metodo serive para crear el registro de la gestion oferta
        @type validated_data: Este campo recibe
        @rtype: object
        """
        detalles_data = validated_data.pop('detalles')
        oferta = Oferta.objects.create(**validated_data)
        for detalle_data in detalles_data:
            OfertaDetalles.objects.create(oferta=oferta, **detalle_data)
        return oferta


# Detalles con imagenes
class DetallesImagenesSerializer(serializers.ModelSerializer):
    # La clase meta se relaciona con la tabla Publicaciones
    # el campo fields indica los campos que se devolveran
    class Meta:
        model = OfertaDetalles
        fields = ['id', 'producto', 'codigo', 'cantidad', 'precio']

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
