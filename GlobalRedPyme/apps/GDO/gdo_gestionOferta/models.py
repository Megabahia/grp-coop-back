from django.db import models


# Nube: bigpuntos
# Portales: CORP
# Esta clase sirve para relacionarse con la tabla oferta
class Oferta(models.Model):
    negocio = models.SmallIntegerField(null=True)
    cliente = models.SmallIntegerField(null=True)
    # codigoOferta = models.CharField(max_length=150,null=True, blank=True)
    fechaOferta = models.DateField(null=True)
    nombres = models.CharField(max_length=150, null=True)
    apellidos = models.CharField(max_length=150, null=True)
    identificacion = models.CharField(max_length=13, null=True)
    telefono = models.CharField(max_length=150, null=True)
    correo = models.EmailField(max_length=150, null=True)
    vigenciaOferta = models.IntegerField(null=True)
    canal = models.CharField(max_length=150, null=True)
    calificacionCliente = models.CharField(max_length=150, null=True)
    indicadorCliente = models.CharField(max_length=150, null=True)
    personaGenera = models.CharField(max_length=150, null=True)
    descripcion = models.TextField(null=True)
    total = models.FloatField(null=True)

    fechaCompra = models.DateField(null=True)
    comunicoOferta = models.CharField(max_length=150, null=True, blank=True)
    fechaComunicacion = models.DateField(null=True)
    aceptoOferta = models.CharField(max_length=150, null=True, blank=True)
    fechaAceptacion = models.DateField(null=True)
    calificacionOferta = models.CharField(max_length=150, null=True, blank=True)
    estado = models.CharField(max_length=150, null=True, blank=True)
    codigo = models.CharField(max_length=150, null=True)
    # Id de la empresa que se inicia sesion
    empresa_id = models.CharField(max_length=255, null=False, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    state = models.SmallIntegerField(default=1)


# Nube: bigpuntos
# Portales: CORP
# Esta clase sirve para relacionarse con la tabla detalles
class OfertaDetalles(models.Model):
    # NOMBRAMOS A LA RELACION DETALLES
    oferta = models.ForeignKey(Oferta, related_name='detalles', null=True, blank=True,
                               on_delete=models.DO_NOTHING)  # Relacion Oferta
    codigo = models.CharField(max_length=150, null=True)
    cantidad = models.PositiveSmallIntegerField(null=True)
    producto = models.CharField(max_length=150, null=True)
    precio = models.FloatField(null=True)
    descuento = models.FloatField(null=True)
    total = models.FloatField(null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    state = models.SmallIntegerField(default=1)

    def save(self, *args, **kwargs):
        return super(OfertaDetalles, self).save(*args, **kwargs)

    def __str__(self):
        return '{}'.format(self.id)
