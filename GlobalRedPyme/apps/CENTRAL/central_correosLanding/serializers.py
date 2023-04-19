from rest_framework import serializers

from apps.CENTRAL.central_correosLanding.models import (
    Correos
)

class CorreosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Correos
       	fields = '__all__'
