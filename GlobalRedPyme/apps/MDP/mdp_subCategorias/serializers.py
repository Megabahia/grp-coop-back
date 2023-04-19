from rest_framework import serializers

from apps.MDP.mdp_subCategorias.models import SubCategorias
from apps.MDP.mdp_categorias.serializers import CategoriasListarSerializer

# LISTAR SUBCATEGORIAS
class ListSubCategoriasSerializer(serializers.ModelSerializer):
    categoria = CategoriasListarSerializer(many=False, read_only=True)
    class Meta:
        model = SubCategorias
       	fields = '__all__'
    def to_representation(self, instance):
        data = super(ListSubCategoriasSerializer, self).to_representation(instance)
        categoria = data.pop('categoria')
        if categoria['nombre']:
            data['categoria'] = categoria['nombre']
        return data

# CREAR Y ACTUALIZAR
class SubCategoriasSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategorias
       	fields = '__all__'

# LISTAR SUB CATEGORIAS COMBO
class SubCategoriasListarSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategorias
       	fields = ['id','nombre']
