from rest_framework import serializers

from .models import (
    FirmaElectronica
)


class FirmaElectronicaSerializer(serializers.ModelSerializer):
    class Meta:
        model = FirmaElectronica
        fields = '__all__'
        read_only_fields = ['_id']
