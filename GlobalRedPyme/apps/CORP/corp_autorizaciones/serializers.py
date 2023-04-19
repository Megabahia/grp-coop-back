from rest_framework import serializers

from .models import (
    Autorizaciones
)


class AutorizacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Autorizaciones
        fields = '__all__'
        read_only_fields = ['_id']

    def to_representation(self, instance):
        data = super(AutorizacionSerializer, self).to_representation(instance)
        # tomo el campo persona y convierto de OBJECTID a string
        cobrar = str(data.pop('cobrar'))
        data.update({"cobrar": cobrar})
        return data
