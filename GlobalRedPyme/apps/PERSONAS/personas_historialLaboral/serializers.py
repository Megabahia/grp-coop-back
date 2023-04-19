from rest_framework import serializers
# ObjectId
from bson import ObjectId

from apps.PERSONAS.personas_historialLaboral.models import (
    HistorialLaboral
)

from apps.CORP.corp_empresas.models import Empresas
from apps.CORP.corp_empresas.serializers import EmpresasInfoBasicaSerializer

class HistorialLaboralSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistorialLaboral
       	fields = '__all__'
        read_only_fields = ['_id']

    def to_representation(self, instance):
        data = super(HistorialLaboralSerializer, self).to_representation(instance)
        # tomo el campo persona y convierto de OBJECTID a string
        empresa = str(data.pop('empresa'))
        empresa = Empresas.objects.filter(pk=ObjectId(empresa),state=1).first()
        if(empresa):
            serializer = EmpresasInfoBasicaSerializer(empresa)
            data['nombreEmpresa'] = serializer.data['nombreEmpresa']
            data['nombreComercial'] = serializer.data['nombreComercial']
            data['imagen'] = serializer.data['imagen']
        return data