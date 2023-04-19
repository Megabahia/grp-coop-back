from rest_framework import serializers

from .models import Catalogo


class CatalogoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Catalogo
        fields = '__all__'
        read_only_fields = ['_id']

    def to_representation(self, instance):
        data = super(CatalogoSerializer, self).to_representation(instance)
        idPadre = str(data['idPadre'])
        data.update({"idPadre": idPadre})
        return data


class CatalogoHijoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Catalogo
        fields = ['_id', 'nombre', 'valor', 'config']
        read_only_fields = ['_id']


class CatalogoListaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Catalogo
        fields = ['_id', 'nombre', 'tipo', 'tipoVariable', 'valor', 'descripcion', 'config']
        read_only_fields = ['_id']


class CatalogoFiltroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Catalogo
        fields = ['_id', 'nombre', 'valor']
        read_only_fields = ['_id']


class CatalogoTipoSerializer(serializers.ModelSerializer):
    # asignamos como nombre al dato tipo en la bd
    valor = serializers.CharField(source='tipo')

    class Meta:
        model = Catalogo
        fields = ['valor']

    def to_representation(self, instance):
        data = super(CatalogoTipoSerializer, self).to_representation(instance)
        # tomo el campo factura y convierto de OBJECTID a string
        catalogo = Catalogo.objects.filter(tipo=data['valor']).order_by('created_at').first()
        _id = str(catalogo._id)
        data.update({"_id": _id})
        return data
