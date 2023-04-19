from rest_framework import serializers
# ObjectId
from bson import ObjectId

from apps.MDM.mdm_facturas.models import FacturasEncabezados, FacturasDetalles
from apps.MDM.mdm_negocios.models import Negocios
from apps.MDM.mdm_clientes.models import Clientes
from apps.MDP.mdp_productos.models import Productos, HistorialAvisos

from datetime import datetime
from django.utils import timezone

# Actualizar factura
class FacturasDetallesSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    class Meta:
        model = FacturasDetalles
       	fields = '__all__'

class FacturasSerializer(serializers.ModelSerializer):
    # id = serializers.IntegerField()
    detalles = FacturasDetallesSerializer(many=True,allow_empty=False)
    class Meta:
        model = FacturasEncabezados
       	fields = '__all__'

    def create(self, validated_data):
        detalles_data = validated_data.pop('detalles')
        facturaEncabezado = FacturasEncabezados.objects.create(**validated_data)
        for detalle_data in detalles_data:
            FacturasDetalles.objects.create(facturaEncabezado=facturaEncabezado, **detalle_data)
        return facturaEncabezado
    
    def update(self, instance, validated_data):
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
                FacturasDetalles.objects.create(**data)
            else:
                now = timezone.localtime(timezone.now())
                data['updated_at'] = str(now)
                FacturasDetalles.objects.filter(id=detalle.id).update(**data)

        return instance

# Listar las facturas cabecera
class FacturasListarSerializer(serializers.ModelSerializer):
    class Meta:
        model = FacturasEncabezados
       	fields = '__all__'

# Listar las facturas cabecera tabla
class FacturasListarTablaSerializer(serializers.ModelSerializer):
    class Meta:
        model = FacturasEncabezados
       	fields = ['id','numeroFactura','created_at','canal','numeroProductosComprados','total']

# Crear factura
class DetallesSerializer(serializers.ModelSerializer):
    class Meta:
        model = FacturasDetalles
       	fields = '__all__'

class FacturaSerializer(serializers.ModelSerializer):
    # id = serializers.IntegerField()
    detalles = DetallesSerializer(many=True,allow_empty=False)
    # content_type = serializers.CharField()
    # object_id = serializers.IntegerField()
    class Meta:
        model = FacturasEncabezados
       	fields = '__all__'

    def create(self, validated_data):
        # if validated_data.get('content_type') == 'negocio':
        #     content = Negocios.objects.get(pk=validated_data.get('object_id'), state=1)
        # if validated_data.get('content_type') == 'cliente':
        #     content = Clientes.objects.get(pk=validated_data.get('object_id'), state=1)
        
        # validated_data.pop('content_type')
        # validated_data.pop('object_id')
        detalles_data = validated_data.pop('detalles')
        # facturaEncabezado = FacturasEncabezados.objects.create(**validated_data,content_object=content)
        facturaEncabezado = FacturasEncabezados.objects.create(**validated_data)
        if facturaEncabezado.numeroFactura is None:
            facturaEncabezado.numeroFactura = facturaEncabezado.id + 1
            facturaEncabezado.save()
        else:
            facturaEncabezado.numeroFactura = 1
            facturaEncabezado.save()
        for detalle_data in detalles_data:
            FacturasDetalles.objects.create(facturaEncabezado=facturaEncabezado, **detalle_data)
            HistorialAvisos.objects.create(codigoBarras=detalle_data['codigo'],fechaCompra=datetime.today().strftime('%Y-%m-%d'),productosVendidos=detalle_data['cantidad'],precioVenta=detalle_data['total'])
        return facturaEncabezado