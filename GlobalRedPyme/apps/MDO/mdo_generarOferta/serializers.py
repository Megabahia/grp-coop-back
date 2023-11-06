from rest_framework import serializers

from .models import Oferta, OfertaDetalles

import requests
from ...config import config
from django.utils import timezone


# Actualizar factura
class OfertasDetallesSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    # La clase meta se relaciona con la tabla Facturas
    # el campo fields indica los campos que se devolveran
    class Meta:
        model = OfertaDetalles
        fields = '__all__'


class OfertasSerializer(serializers.ModelSerializer):
    # id = serializers.IntegerField()
    detalles = OfertasDetallesSerializer(many=True, allow_empty=False)

    # La clase meta se relaciona con la tabla Facturas
    # el campo fields indica los campos que se devolveran
    class Meta:
        model = Oferta
        fields = '__all__'

    def create(self, validated_data):
        """
        ESte metodo sirve para crear la oferta
        @type validated_data: El campo validated_data recibe los datos para registrar en la tabla oferta
        @rtype: Devuelve el registro creado
        """
        detalles_data = validated_data.pop('detalles')
        oferta = Oferta.objects.create(**validated_data)
        for detalle_data in detalles_data:
            OfertaDetalles.objects.create(oferta=oferta, **detalle_data)
        return oferta

    def update(self, instance, validated_data):
        """
        ESte metodo sirve para actualizar la oferta
        @type instance: El campo instance recibe la informacion de la tabla oferta
        @type validated_data: El campo validated_data recibe los datos para registrar en la tabla oferta
        @rtype: Devuelve el registro actualizado
        """
        detalles_database = {detalle.id: detalle for detalle in instance.detalles.all()}
        detalles_actualizar = {item['id']: item for item in validated_data['detalles']}
        # data_mapping = {item['id']: item for item in validated_data.pop('detalles')}

        # Actualiza la factura cabecera
        instance.__dict__.update(validated_data)
        instance.save()

        # Eliminar los detalles que no esté incluida en la solicitud de la factura detalles
        for detalle in instance.detalles.all():
            if detalle.id not in detalles_actualizar:
                detalle.delete()

        # Crear o actualizar instancias de detalles que se encuentran en la solicitud de factura detalles
        for detalle_id, data in detalles_actualizar.items():
            detalle = detalles_database.get(detalle_id, None)
            if detalle is None:
                data.pop('id')
                OfertaDetalles.objects.create(**data)
            else:
                now = timezone.localtime(timezone.now())
                data['updated_at'] = str(now)
                OfertaDetalles.objects.filter(id=detalle.id).update(**data)

        return instance


# Listar las facturas cabecera
class OfertasListarSerializer(serializers.ModelSerializer):
    # La clase meta se relaciona con la tabla Facturas
    # el campo fields indica los campos que se devolveran
    class Meta:
        model = Oferta
        fields = '__all__'


# Listar oferta cabecera tabla
class OfertasListarTablaSerializer(serializers.ModelSerializer):
    # La clase meta se relaciona con la tabla Facturas
    # el campo fields indica los campos que se devolveran
    class Meta:
        model = Oferta
        fields = ['id', 'identificacion', 'numeroFactura', 'fecha', 'nombres', 'apellidos', 'telefono', 'correo',
                  'indicadorCliente', 'calificacionCliente', 'vigenciaOferta', 'canal', 'total']


# Crear factura
class DetallesSerializer(serializers.ModelSerializer):
    # La clase meta se relaciona con la tabla Facturas
    # el campo fields indica los campos que se devolveran
    class Meta:
        model = OfertaDetalles
        fields = '__all__'


class OfertaSerializer(serializers.ModelSerializer):
    detalles = DetallesSerializer(many=True, allow_empty=False)

    # La clase meta se relaciona con la tabla Facturas
    # el campo fields indica los campos que se devolveran
    class Meta:
        model = Oferta
        fields = '__all__'

    def create(self, validated_data):
        """
        ESte metodo sirve para crear la oferta
        @type validated_data: El campo validated_data recibe los datos para registrar en la tabla oferta
        @rtype: Devuelve el registro creado
        """
        detalles_data = validated_data.pop('detalles')
        oferta = Oferta.objects.create(**validated_data)
        for detalle_data in detalles_data:
            OfertaDetalles.objects.create(oferta=oferta, **detalle_data)
        return oferta


# Detalles con imagenes
class DetallesImagenesSerializer(serializers.ModelSerializer):
    # La clase meta se relaciona con la tabla Facturas
    # el campo fields indica los campos que se devolveran
    class Meta:
        model = OfertaDetalles
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
