from rest_framework import serializers

from .models import (
    RucPersonas
)


class RucPersonasSerializer(serializers.ModelSerializer):
    class Meta:
        model = RucPersonas
        fields = '__all__'
        read_only_fields = ['_id']
