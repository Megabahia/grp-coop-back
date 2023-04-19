from rest_framework import serializers

from .models import (
    Proveedores
)


class ProveedoresSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proveedores
        fields = '__all__'
        read_only_fields = ['_id']
