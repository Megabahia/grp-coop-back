from django.db import models


# Mundo: Bigpuntos
# Portales: Corp
# Esta clase se relaciona con la tabla oferta de la base datos mdo
class Oferta(models.Model):
    negocio = models.SmallIntegerField(null=True)
    cliente = models.SmallIntegerField(null=True)
    numeroFactura = models.CharField(max_length=150, null=True, blank=True)
    fecha = models.DateField(null=True)
    tipoIdentificacion = models.CharField(max_length=150, null=True)
    identificacion = models.CharField(max_length=13, null=True)
    razonSocial = models.CharField(max_length=255, null=True)
    direccion = models.CharField(max_length=255, null=True)
    telefono = models.CharField(max_length=150, null=True)
    correo = models.EmailField(max_length=255, null=True)
    nombreVendedor = models.CharField(max_length=255, null=True)
    subTotal = models.FloatField(null=True)
    descuento = models.FloatField(null=True)
    iva = models.FloatField(null=True)
    total = models.FloatField(null=True)
    canal = models.CharField(max_length=255, null=True)
    numeroProductosComprados = models.IntegerField(null=True)

    nombres = models.CharField(max_length=255, null=True)
    apellidos = models.CharField(max_length=255, null=True)
    vigenciaOferta = models.PositiveIntegerField(null=True)
    calificacionCliente = models.CharField(max_length=150, null=True)
    indicadorCliente = models.CharField(max_length=150, null=True)
    descripcion = models.TextField(null=True)
    # Id de la empresa que se inicia sesion
    empresa_id = models.CharField(max_length=255, null=False, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    state = models.SmallIntegerField(default=1)


class OfertaDetalles(models.Model):
    # NOMBRAMOS A LA RELACION DETALLES
    oferta = models.ForeignKey(Oferta, related_name='detalles', null=True, blank=True,
                               on_delete=models.DO_NOTHING)  # Relacion Oferta
    producto = models.CharField(max_length=255, null=True)
    valorUnitario = models.FloatField(null=True)
    cantidad = models.PositiveIntegerField(null=True)
    precio = models.FloatField(null=True)
    codigo = models.CharField(max_length=255, null=True)
    informacionAdicional = models.TextField(null=True)
    descuento = models.FloatField(null=True)
    impuesto = models.FloatField(null=True)
    valorDescuento = models.FloatField(null=True)
    total = models.FloatField(null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    state = models.SmallIntegerField(default=1)

    def __str__(self):
        return '{}'.format(self.id)
