from djongo import models


# Create your models here.
class MovimientoCobros(models.Model):
    _id = models.ObjectIdField()
    autorizacion = models.IntegerField(null=True, blank=True)
    codigoCobro = models.CharField(max_length=200, null=True, blank=True)
    fechaCobro = models.DateField(null=True, blank=True)
    montoTotalFactura = models.FloatField(null=True, blank=True)
    montoSupermonedas = models.FloatField(null=True, blank=True)
    user_id = models.CharField(max_length=250, blank=True, null=True)  # Relacion usuario
    empresa_id = models.CharField(max_length=250, blank=True, null=True)  # Relacion empresa

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    state = models.SmallIntegerField(default=1)
