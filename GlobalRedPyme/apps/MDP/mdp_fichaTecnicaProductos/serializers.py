from rest_framework import serializers

from .models import FichaTecnicaProductos


class FichaTecnicaProductosSerializer(serializers.ModelSerializer):
    # La clase meta se relaciona con la tabla FichaTecnicaProductos
    # el campo fields indica los campos que se devolveran
    class Meta:
        model = FichaTecnicaProductos
        fields = '__all__'
