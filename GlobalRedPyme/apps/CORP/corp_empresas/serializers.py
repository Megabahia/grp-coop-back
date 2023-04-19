from rest_framework import serializers

from .models import (
    Empresas, EmpresasConvenio, Empleados
)


class EmpresasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Empresas
        fields = '__all__'
        read_only_fields = ['_id']


class EmpresasInfoBasicaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Empresas
        fields = ['_id', 'nombreEmpresa', 'imagen', 'nombreComercial']


class EmpresasFiltroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Empresas
        fields = ['_id', 'nombreEmpresa', 'ruc', 'tipoEmpresa', 'tipoCategoria']


class EmpresasFiltroIfisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Empresas
        fields = ['_id', 'nombreEmpresa', 'nombreComercial', 'tipoCategoria', 'ruc']


class EmpresasConvenioCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmpresasConvenio
        fields = '__all__'
        read_only_fields = ['_id']

    def to_representation(self, instance):
        data = super(EmpresasConvenioCreateSerializer, self).to_representation(instance)
        # tomo el campo persona y convierto de OBJECTID a string
        convenio = str(data.pop('convenio'))
        data.update({"convenio": convenio})
        return data


class EmpresasConvenioSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmpresasConvenio
        fields = ['convenio']

    def to_representation(self, instance):
        data = super(EmpresasConvenioSerializer, self).to_representation(instance)
        # tomo el campo persona y convierto de OBJECTID a string
        convenio = data.pop('convenio')
        empresa = Empresas.objects.filter(_id=convenio, state=1).first()
        data.update(EmpresasSerializer(empresa).data)
        return data


class EmpresasLogosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Empresas
        fields = ['imagen']


class EmpleadosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Empleados
        fields = '__all__'
        read_only_fields = ['_id']

    def to_representation(self, instance):
        data = super(EmpleadosSerializer, self).to_representation(instance)
        # tomo el campo persona y convierto de OBJECTID a string
        empresa = data.pop('empresa')
        empresa = Empresas.objects.filter(_id=empresa, state=1).first()
        if empresa is not None:
            data['ruc'] = (EmpresasSerializer(empresa).data['ruc'])
            data['nombreComercial'] = (EmpresasSerializer(empresa).data['nombreComercial'])
        return data
