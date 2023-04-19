from django.db import models

# from django.contrib.contenttypes.fields import GenericForeignKey
# from django.contrib.contenttypes.models import ContentType

from apps.MDM.mdm_negocios.models import Negocios
from apps.MDM.mdm_clientes.models import Clientes

# Create your models here.
class FacturasEncabezados(models.Model):
    negocio= models.ForeignKey(Negocios, null=True, blank=True, on_delete=models.DO_NOTHING)  # Relacion Negocios
    cliente= models.ForeignKey(Clientes, null=True, blank=True, on_delete=models.DO_NOTHING)  # Relacion Clientes
    numeroFactura = models.CharField(max_length=150,null=True, blank=True)
    fecha = models.DateField(null=True)
    tipoIdentificacion = models.CharField(max_length=150,null=True)
    identificacion = models.CharField(max_length=150,null=True)
    razonSocial = models.CharField(max_length=150,null=True)
    direccion = models.CharField(max_length=150,null=True)
    telefono = models.CharField(max_length=150,null=True)
    correo = models.EmailField(max_length=150,null=True)
    nombreVendedor = models.CharField(max_length=150,null=True)
    subTotal = models.FloatField(null=True)
    descuento = models.FloatField(null=True)
    iva = models.FloatField(null=True)
    total = models.FloatField(null=True)
    canal = models.CharField(max_length=150,null=True)
    numeroProductosComprados = models.IntegerField(null=True)
    # Id de la empresa que se inicia sesion
    empresa_id = models.CharField(max_length=255,null=False, blank=True)
        
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    state = models.SmallIntegerField(default=1)

    # Relacion polimorfica
    # Hace referencia al modelo que vamos a utulizar
    # content_type = models.ForeignKey(ContentType, null=True, blank=True, on_delete=models.DO_NOTHING) 
    # # Hace referencia al id del objeto a almacenar
    # object_id = models.PositiveIntegerField(null=True, blank=True,)

    # content_object = GenericForeignKey(
    #     'content_type', 
    #     'object_id' 
    # )

    def save(self, *args, **kwargs):
        # self.tipo = self.tipo.upper()
        return super(FacturasEncabezados, self).save(*args, **kwargs)

    # def __str__(self):
    #     return '{}'.format(self.nombres)


class FacturasDetalles(models.Model):
    # NOMBRAMOS A LA RELACION DETALLATES
    facturaEncabezado= models.ForeignKey(FacturasEncabezados, related_name='detalles', null=True, blank=True, on_delete=models.DO_NOTHING)  # Relacion Factura
    articulo = models.CharField(max_length=150,null=True)
    valorUnitario = models.FloatField(null=True)
    cantidad = models.PositiveIntegerField(null=True)
    precio = models.FloatField(null=True)
    codigo = models.CharField(max_length=250,null=True)
    informacionAdicional = models.CharField(max_length=250,null=True)
    descuento = models.FloatField(null=True)
    impuesto = models.FloatField(null=True)
    valorDescuento = models.FloatField(null=True)
    total = models.FloatField(null=True)
        
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    state = models.SmallIntegerField(default=1)

    def save(self, *args, **kwargs):
        # self.tipo = self.tipo.upper()
        return super(FacturasDetalles, self).save(*args, **kwargs)

    def __str__(self):
        return '{}'.format(self.id)