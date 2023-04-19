from rest_framework import serializers

from apps.MDP.mdp_productos.models import (
    Productos, ProductoImagen,
    ReporteAbastecimiento, ReporteStock, ReporteCaducidad, ReporteRotacion,
    HistorialAvisos
)

import datetime
from django.utils import timezone

class ProductosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Productos
       	fields = '__all__'

# LISTAR PRODUCTOS TABLA
class ProductosListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Productos
       	fields = ['id','codigoBarras','nombre','categoria','subCategoria','stock','estado']

# DETALLES IMAGENES
class DetallesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductoImagen
       	fields = '__all__'

# IMAGEN URL
class ImagenSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductoImagen
       	fields = ['imagen',]

# CREAR PRODUCTO
class ProductoCreateSerializer(serializers.ModelSerializer):
    imagenes = DetallesSerializer(many=True,required=False,allow_null=True,allow_empty=True)
    class Meta:
        model = Productos
       	fields = '__all__'

    def create(self, validated_data):
        if "imagenes" in validated_data:
            detalles_data = validated_data.pop('imagenes')
            producto = Productos.objects.create(**validated_data)
            for detalle_data in detalles_data:
                ProductoImagen.objects.create(producto=producto, **detalle_data)
        else:
            producto = Productos.objects.create(**validated_data)
        return producto

# ACTUALIZAR PRODUCTO
class DetallesImagenesSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    class Meta:
        model = ProductoImagen
       	fields = '__all__'

class ProductosActualizarSerializer(serializers.ModelSerializer):
    imagenes = DetallesImagenesSerializer(many=True,required=False,allow_null=True,allow_empty=True)
    class Meta:
        model = Productos
       	fields = '__all__'

    def create(self, validated_data):        
        detalles_data = validated_data.pop('imagenes')
        producto = Productos.objects.create(**validated_data)
        for detalle_data in detalles_data:
            ProductoImagen.objects.create(producto=producto, **detalle_data)
        return producto
    
    def update(self, instance, validated_data):
        if "imagenes" in validated_data:
            detalles_database = {detalle.id: detalle for detalle in instance.imagenes.all()}
            detalles_actualizar = {item['id']: item for item in validated_data['imagenes']}

            # Actualiza el producto
            instance.__dict__.update(validated_data) 
            instance.save()

            # Eliminar los imagenes que no esté incluida en la solicitud de la productos imagenes
            for detalle in instance.imagenes.all():
                if detalle.id not in detalles_actualizar:
                    detalle.imagen.delete()
                    detalle.delete()

            # Crear o actualizar instancias de imagenes que se encuentran en la solicitud de producto imagenes
            for detalle_id, data in detalles_actualizar.items():
                detalle = detalles_database.get(detalle_id, None)
                if detalle is None:
                    data.pop('id')
                    data['producto_id']=instance.id
                    ProductoImagen.objects.create(**data)
                # else:
                #     now = timezone.localtime(timezone.now())
                #     data['updated_at'] = str(now)
                #     ProductoImagen.objects.filter(id=detalle.id).update(**data)
        else:
            # Actualiza el producto
            instance.__dict__.update(validated_data) 
            instance.save()

        return instance

# ABASTECIMIENTO
class AbastecimientoListSerializer(serializers.ModelSerializer):
    producto = ProductosSerializer(many=False, read_only=True)
    class Meta:
        model = ReporteAbastecimiento
       	fields = '__all__'
    def to_representation(self, instance):
        data = super(AbastecimientoListSerializer, self).to_representation(instance)
        producto = data.pop('producto')
        if producto['codigoBarras']:
            data['codigoBarras'] = producto['codigoBarras']
        if producto['nombre']:
            data['nombre'] = producto['nombre']
        if producto['categoria']:
            data['categoria'] = producto['categoria']
        if producto['subCategoria']:
            data['subCategoria'] = producto['subCategoria']
        if producto['stock']:
            data['stock'] = producto['stock']
        if producto['parametrizacion']:
            data['alertaAbastecimiento'] = instance.producto.parametrizacion.nombre
        return data

# HISTORIAL ABASTECIMIENTO
class HistorialAvisosSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistorialAvisos
       	fields = '__all__'

# STOCK
class StockListSerializer(serializers.ModelSerializer):
    producto = ProductosSerializer(many=False, read_only=True)
    class Meta:
        model = ReporteStock
       	fields = '__all__'
    def to_representation(self, instance):
        data = super(StockListSerializer, self).to_representation(instance)
        producto = data.pop('producto')
        if producto['codigoBarras']:
            data['codigoBarras'] = producto['codigoBarras']
        if producto['nombre']:
            data['nombre'] = producto['nombre']
        if producto['categoria']:
            data['categoria'] = producto['categoria']
        if producto['subCategoria']:
            data['subCategoria'] = producto['subCategoria']
        if producto['stock']:
            data['stock'] = producto['stock']
        return data

# CADUCIDAD
class CaducidadListSerializer(serializers.ModelSerializer):
    producto = ProductosSerializer(many=False, read_only=True)
    class Meta:
        model = ReporteCaducidad
       	fields = '__all__'
    def to_representation(self, instance):
        diasParaCaducar = (instance.producto.fechaCaducidad - datetime.datetime.now().date()).days
        if int(diasParaCaducar) > 0:
            instance.diasParaCaducar = diasParaCaducar
            instance.productosCaducados = 0
        else:
            instance.diasParaCaducar = 0
            instance.productosCaducados = instance.producto.stock
        instance.save()
        data = super(CaducidadListSerializer, self).to_representation(instance)        
        producto = data.pop('producto')
        if producto['codigoBarras']:
            data['codigoBarras'] = producto['codigoBarras']
        if producto['nombre']:
            data['nombre'] = producto['nombre']
        if producto['categoria']:
            data['categoria'] = producto['categoria']
        if producto['subCategoria']:
            data['subCategoria'] = producto['subCategoria']
        return data

# ROTACION
class RotacionListSerializer(serializers.ModelSerializer):
    producto = ProductosSerializer(many=False, read_only=True)
    class Meta:
        model = ReporteRotacion
       	fields = '__all__'
    def to_representation(self, instance):
        data = super(RotacionListSerializer, self).to_representation(instance)
        producto = data.pop('producto')
        if producto['codigoBarras']:
            data['codigoBarras'] = producto['codigoBarras']
        if producto['nombre']:
            data['nombre'] = producto['nombre']
        if producto['categoria']:
            data['categoria'] = producto['categoria']
        if producto['subCategoria']:
            data['subCategoria'] = producto['subCategoria']
        return data

# REFIL
class RefilListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Productos
       	fields = ['id','codigoBarras','nombre','categoria','subCategoria','refil','variableRefil']

# PREDICCION PRODUCTOS CROSSELING
class PrediccionCrosselingSerializer(serializers.ModelSerializer):
    producto = ProductosSerializer(many=False, read_only=True)    
    class Meta:
        model = ReporteRotacion
       	fields = ['producto']
    def to_representation(self, instance):
        data = super(PrediccionCrosselingSerializer, self).to_representation(instance)
        producto = data.pop('producto')
        if producto['codigoBarras']:
            data['codigoBarras'] = producto['codigoBarras']
        if producto['nombre']:
            data['nombre'] = producto['nombre']
        if producto['precioVentaA']:
            data['precioVentaA'] = producto['precioVentaA']
        if producto['precioVentaB']:
            data['precioVentaB'] = producto['precioVentaB']
        if producto['precioVentaC']:
            data['precioVentaC'] = producto['precioVentaC']
        if producto['precioVentaD']:
            data['precioVentaD'] = producto['precioVentaD']
        if producto['precioVentaE']:
            data['precioVentaE'] = producto['precioVentaE']
        if instance.producto.imagenes.first():
            data['imagen'] = str(instance.producto.imagenes.first().imagen)
        return data

# OBTENER PRODUCTOS REFIL
class PrediccionRefilSerializer(serializers.ModelSerializer): 
    class Meta:
        model = Productos
       	fields = ['codigoBarras','refil']


# PREDICCION PRODUCTOS CROSSELING
class PrediccionRefilOneSerializer(serializers.ModelSerializer):  
    producto = ProductosSerializer(many=False, read_only=True)    
    class Meta:
        model = ProductoImagen
       	fields = ['producto']
    def to_representation(self, instance):
        data = super(PrediccionRefilOneSerializer, self).to_representation(instance)
        producto = data.pop('producto')
        if producto['codigoBarras']:
            data['codigoBarras'] = producto['codigoBarras']
        if producto['nombre']:
            data['nombre'] = producto['nombre']
        if producto['precioVentaA']:
            data['precioVentaA'] = producto['precioVentaA']
        if producto['precioVentaB']:
            data['precioVentaB'] = producto['precioVentaB']
        if producto['precioVentaC']:
            data['precioVentaC'] = producto['precioVentaC']
        if producto['precioVentaD']:
            data['precioVentaD'] = producto['precioVentaD']
        if producto['precioVentaE']:
            data['precioVentaE'] = producto['precioVentaE']
        if instance.producto.imagenes.first():
            data['imagen'] = str(instance.producto.imagenes.first().imagen)
        return data

# BUSQUEDA POR CODIGO
class ProductoSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Productos
       	fields = ['id','codigoBarras','nombre','precioVentaA','precioVentaB','precioVentaC','precioVentaD','precioVentaE']
    def to_representation(self, instance):
        data = super(ProductoSearchSerializer, self).to_representation(instance)
        imagen = ProductoImagen.objects.filter(producto=instance).first()
        if imagen is not None:
            data['imagen'] = ImagenSerializer(imagen).data['imagen']
        return data
