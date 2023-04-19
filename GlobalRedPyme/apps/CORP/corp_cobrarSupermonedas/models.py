from djongo import models


# Create your models here.
class CobrarSupermonedas(models.Model):
    _id = models.ObjectIdField()
    identificacion = models.CharField(max_length=13, null=False)
    codigoCobro = models.CharField(max_length=200, null=False)
    monto = models.FloatField(null=True)
    correo = models.EmailField(max_length=200, null=False)
    estado = models.CharField(max_length=200, null=False)
    user_id = models.CharField(max_length=250, blank=False, null=False)  # Relacion usuario

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    state = models.SmallIntegerField(default=1)
