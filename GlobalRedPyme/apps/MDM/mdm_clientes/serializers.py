from rest_framework import serializers

from apps.MDM.mdm_clientes.models import Clientes, DatosFisicosClientes, DatosVirtualesClientes, Parientes


class ClientesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clientes
       	fields = '__all__'

class ClientesUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clientes
       	exclude = ('imagen',)

class ClientesListarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clientes
       	fields = ['id','nombreCompleto','nombres','apellidos','correo']

class ClienteImagenSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Clientes
        fields = ['imagen','updated_at']

class DatosFisicosClientesSerializer(serializers.ModelSerializer):
    class Meta:
        model = DatosFisicosClientes
       	fields = '__all__'

class DatosVirtualesClientesSerializer(serializers.ModelSerializer):
    class Meta:
        model = DatosVirtualesClientes
       	fields = '__all__'

class ParientesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parientes
       	fields = '__all__'

class TablaParientesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parientes
       	fields = ['id','created_at','tipoPariente','nombres','apellidos','edad','celularPersonal','correoPersonal']

class ClientePrediccionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clientes
       	fields = ['id','nombreCompleto','correo','cedula','estado','paisNacimiento','imagen']


