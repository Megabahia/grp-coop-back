from rest_framework import serializers

from .models import Categorias


class CategoriasSerializer(serializers.ModelSerializer):
    # La clase meta se relaciona con la tabla Facturas
    # el campo fields indica los campos que se devolveran
    class Meta:
        model = Categorias
        fields = '__all__'


# LISTAR NEGOCIOS
class CategoriasListarSerializer(serializers.ModelSerializer):
    # La clase meta se relaciona con la tabla Facturas
    # el campo fields indica los campos que se devolveran
    class Meta:
        model = Categorias
        fields = ['id', 'nombre']
