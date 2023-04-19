from rest_framework import serializers

from apps.MDP.mdp_categorias.models import Categorias


class CategoriasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categorias
       	fields = '__all__'

# LISTAR NEGOCIOS
class CategoriasListarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categorias
       	fields = ['id','nombre']