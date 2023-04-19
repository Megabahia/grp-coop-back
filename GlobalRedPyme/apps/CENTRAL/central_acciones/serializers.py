from rest_framework import serializers

from apps.CENTRAL.central_acciones.models import Acciones,AccionesPermitidas,AccionesPorRol

class AccionesPadreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Acciones
       	fields = ['id', 'codigo', 'nombre']


class AccionesSerializer(serializers.ModelSerializer):
    idAccionPadre = AccionesPadreSerializer(many=False, read_only=True)
    class Meta:
        model = Acciones
        fields = '__all__'
    def to_representation(self, instance):
        data = super(AccionesSerializer, self).to_representation(instance)
        accionPadre = data.pop('idAccionPadre')
        if accionPadre['codigo']:
            data={'codigoPadre':accionPadre['codigo'],
            'info':data
            }
        return data

class AccionesPermitidasSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccionesPermitidas
       	fields = '__all__'

class AccionesPorRolSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccionesPorRol
       	fields = '__all__'

