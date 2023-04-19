from djongo import models

# Create your models here.
class Correos(models.Model):
    fechaRegistro = models.DateField(auto_now_add=True)
    correo = models.EmailField(max_length=255,null=False, blank=False)
    correoValido = models.BooleanField(default=False)
    codigoValido = models.BooleanField(default=False)
    accedio = models.BooleanField(default=False)
    codigo = models.CharField(max_length=255,null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    state = models.SmallIntegerField(default=1)