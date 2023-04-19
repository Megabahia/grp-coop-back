from rest_framework import serializers

from .models import (
    PagoProveedores
)

class PagoProveedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = PagoProveedores
        fields = '__all__'
        read_only_fields = ['_id']
