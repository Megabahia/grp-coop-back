from djongo import models


# Create your models here.
class FirmaElectronica(models.Model):
    _id = models.ObjectIdField()
    nombreRepresentante = models.CharField(max_length=255, null=True, blank=True)
    apellidoRepresentante = models.CharField(max_length=255, null=True, blank=True)
    correoRepresentante = models.CharField(max_length=255, null=True, blank=True)
    telefonoRepresentante = models.CharField(max_length=255, null=True, blank=True)
    whatsappRepresentante = models.CharField(max_length=255, null=True, blank=True)
    tipoIdentificacionRepresentante = models.CharField(max_length=255, null=True, blank=True)
    identificacionRepresentante = models.CharField(max_length=255, null=True, blank=True)
    aceptarTerminos = models.BooleanField(default=False)
    user_id = models.CharField(max_length=255, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    state = models.SmallIntegerField(default=1)
