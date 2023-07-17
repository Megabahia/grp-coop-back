import jsonfield
from django.utils import timezone
from djongo import models


def upload_path(instance, filname):
    return '/'.join(['CORP/documentosCreditosArchivos', str(timezone.localtime(timezone.now())) + "_" + filname])


# Create your models here.
class PagoEmpleados(models.Model):
    _id = models.ObjectIdField()
    nombresCompletos = models.CharField(max_length=255, null=True, blank=True)
    cedula = models.CharField(max_length=255, null=True, blank=True)
    celular = models.CharField(max_length=255, null=True, blank=True)
    correo = models.EmailField(max_length=255, null=True, blank=True)
    montoPagar = models.CharField(max_length=255, null=True, blank=True)
    codigoEmpleado = models.CharField(max_length=255, null=True, blank=True)
    mesPago = models.CharField(max_length=255, null=True, blank=True)
    anio = models.CharField(max_length=255, null=True, blank=True)
    estado = models.CharField(max_length=255, null=True, blank=True)
    archivoFirmado = models.FileField(blank=True, null=True, upload_to=upload_path)
    fechaFirma = models.DateTimeField(null=True, blank=True)
    user_id = models.CharField(max_length=255, null=True, blank=True)
    observacion = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    state = models.SmallIntegerField(default=1)
