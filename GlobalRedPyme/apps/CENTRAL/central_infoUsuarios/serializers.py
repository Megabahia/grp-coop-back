from rest_framework import serializers

from apps.CENTRAL.central_infoUsuarios.models import InfoUsuarios

class InfoUsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = InfoUsuarios
        fields = '__all__'
        read_only_fields = ['_id']
    
    def to_representation(self, instance):
        data = super(InfoUsuarioSerializer, self).to_representation(instance)
        # convierto a str tipoUsuario
        usuario = str(data.pop('usuario'))
        data.update({"usuario": usuario})
        return data
