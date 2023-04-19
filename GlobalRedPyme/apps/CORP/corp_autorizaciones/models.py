from djongo import models
from ...CORP.corp_cobrarSupermonedas.models import CobrarSupermonedas


# Create your models here.
class Autorizaciones(models.Model):
    _id = models.ObjectIdField()
    codigoAutorizacion = models.CharField(max_length=200, null=False)
    estado = models.CharField(max_length=200, null=False)
    user_id = models.CharField(max_length=250, blank=False, null=False)  # Relacion usuario
    cobrar = models.ForeignKey(CobrarSupermonedas, null=False, on_delete=models.DO_NOTHING)  # Relacion Con la categoria

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    state = models.SmallIntegerField(default=1)
