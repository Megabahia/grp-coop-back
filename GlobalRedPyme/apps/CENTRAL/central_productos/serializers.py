from rest_framework import serializers
# ObjectId
from bson import ObjectId

from apps.CORP.corp_empresas.models import Empresas
from apps.CORP.corp_empresas.serializers import EmpresasSerializer

from apps.CENTRAL.central_productos.models import (
    Productos
)

class ProductosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Productos
       	fields = '__all__'

    def to_representation(self, instance):
        data = super(ProductosSerializer, self).to_representation(instance)
        empresa_id = data.pop('empresa_id')
        empresa = Empresas.objects.get(pk=ObjectId(empresa_id))
        if empresa:
            data['empresa'] = empresa.nombreComercial
            data['local'] = empresa.direccion
            data['pais'] = empresa.pais
            data['provincia'] = empresa.provincia
            data['ciudad'] = empresa.ciudad
            data['imagen_empresa'] = EmpresasSerializer(empresa).data['imagen']
        return data

class ProductosImagenSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Productos
        fields = ['imagen','updated_at']
