from djongo import models


# Create your models here.
class Envios(models.Model):
    _id = models.ObjectIdField()
    numeroEnvio = models.CharField(max_length=13, null=True, blank=True)
    fechaEnvio = models.DateField(null=True, blank=True)
    courierResponsable = models.EmailField(null=True, blank=True)
    direccionEntrega = models.CharField(max_length=255, null=True, blank=True)
    cooperativaEntrega = models.CharField(max_length=255, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    state = models.SmallIntegerField(default=1)
