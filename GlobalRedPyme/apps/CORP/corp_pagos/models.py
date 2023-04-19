from djongo import models
import jsonfield

# Create your models here.
class Pagos(models.Model):
    _id = models.ObjectIdField()
    codigoCobro = models.CharField(max_length=200,null=True,blank=True)
    duracion = models.DateTimeField(null=True,blank=True)
    monto = models.FloatField(null=True,blank=True)
    user_id = models.CharField(max_length=250,blank=True, null=True)  # Relacion usuario
    user = jsonfield.JSONField()
    empresa_id = models.CharField(max_length=250,blank=True, null=True)  # Relacion empresa
    empresa = jsonfield.JSONField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    state = models.SmallIntegerField(default=1)