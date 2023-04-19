from rest_framework import serializers

from apps.PERSONAS.personas_personas.models import (
    Personas, ValidarCuenta
)

class PersonasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Personas
       	fields = '__all__'
        read_only_fields = ['_id']

class PersonasUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Personas
        fields = '__all__'
        read_only_fields = ['user_id']

class PersonasUpdateSinImagenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Personas
        exclude = ['imagen']

class PersonasImagenSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Personas
        fields = ['imagen','updated_at']

class ValidarCuentaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ValidarCuenta
       	fields = '__all__'
        read_only_fields = ['_id']


class PersonasSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Personas
        fields = ['_id','identificacion','nombres','apellidos','user_id','whatsapp']

