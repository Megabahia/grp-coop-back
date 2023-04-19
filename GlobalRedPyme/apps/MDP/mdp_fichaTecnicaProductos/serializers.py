from rest_framework import serializers

from apps.MDP.mdp_fichaTecnicaProductos.models import FichaTecnicaProductos


class FichaTecnicaProductosSerializer(serializers.ModelSerializer):
    class Meta:
        model = FichaTecnicaProductos
       	fields = '__all__'