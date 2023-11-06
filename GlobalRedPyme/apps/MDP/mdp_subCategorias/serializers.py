from rest_framework import serializers

from .models import SubCategorias
from ..mdp_categorias.serializers import CategoriasListarSerializer


# LISTAR SUBCATEGORIAS
class ListSubCategoriasSerializer(serializers.ModelSerializer):
    categoria = CategoriasListarSerializer(many=False, read_only=True)

    # La clase meta se relaciona con la tabla SubCategorias
    # el campo fields indica los campos que se devolveran
    class Meta:
        model = SubCategorias
        fields = '__all__'

    def to_representation(self, instance):
        """
        Este metodo se usa para modificar la respuesta de los campos
        @type instance: El campo instance contiene el registro con los campos
        @rtype: DEvuelve los valores modificados
        """
        data = super(ListSubCategoriasSerializer, self).to_representation(instance)
        categoria = data.pop('categoria')
        if categoria['nombre']:
            data['categoria'] = categoria['nombre']
        return data


# CREAR Y ACTUALIZAR
class SubCategoriasSerializer(serializers.ModelSerializer):
    # La clase meta se relaciona con la tabla SubCategorias
    # el campo fields indica los campos que se devolveran
    class Meta:
        model = SubCategorias
        fields = '__all__'


# LISTAR SUB CATEGORIAS COMBO
class SubCategoriasListarSerializer(serializers.ModelSerializer):
    # La clase meta se relaciona con la tabla SubCategorias
    # el campo fields indica los campos que se devolveran
    class Meta:
        model = SubCategorias
        fields = ['id', 'nombre']
