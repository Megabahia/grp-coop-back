from rest_framework import serializers

from .models import (
    MovimientoCobros
)


class MovimientoCobrosSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovimientoCobros
        fields = '__all__'
        read_only_fields = ['_id']
