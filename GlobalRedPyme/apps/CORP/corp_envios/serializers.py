from rest_framework import serializers

from .models import (
    Envios
)


class EnviosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Envios
        fields = '__all__'
        read_only_fields = ['_id']
