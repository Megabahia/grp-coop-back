import jsonfield
from djongo import models


def upload_path(instance, filname):
    return '/'.join(['PERSONAS/imgPersonas', str(instance._id) + "_" + filname])


# Create your models here.
class Personas(models.Model):
    _id = models.ObjectIdField()
    identificacion = models.CharField(max_length=200, null=True, blank=True)
    nombres = models.CharField(max_length=200, null=True, blank=True)
    apellidos = models.CharField(max_length=200, null=True, blank=True)
    nombresCompleto = models.CharField(max_length=255, null=True, blank=True)
    genero = models.CharField(max_length=200, null=True, blank=True)
    fechaNacimiento = models.DateField(null=True, blank=True)
    edad = models.SmallIntegerField(null=True, blank=True)
    ciudad = models.CharField(max_length=200, null=True, blank=True)
    provincia = models.CharField(max_length=200, null=True, blank=True)
    pais = models.CharField(max_length=200, null=True, blank=True)
    direccion = models.CharField(max_length=255, null=True, blank=True)
    email = models.CharField(max_length=250, blank=True, null=True)
    emailAdicional = models.CharField(max_length=250, blank=True, null=True)
    telefono = models.CharField(max_length=20, null=True, blank=True)
    whatsapp = models.CharField(max_length=150, null=True, blank=True)
    facebook = models.CharField(max_length=250, blank=True, null=True)
    instagram = models.CharField(max_length=250, blank=True, null=True)
    twitter = models.CharField(max_length=250, blank=True, null=True)
    tiktok = models.CharField(max_length=250, blank=True, null=True)
    youtube = models.CharField(max_length=250, blank=True, null=True)
    imagen = models.FileField(blank=True, null=True, upload_to=upload_path)
    user_id = models.CharField(max_length=250, blank=False, null=False)  # Relacion usuario
    empresaInfo = jsonfield.JSONField()
    datosPyme = jsonfield.JSONField()
    estadoCivil = models.CharField(max_length=250, blank=True, null=True)
    cedulaRepresentante = models.CharField(max_length=250, blank=True, null=True)
    direccionRepresentante = models.CharField(max_length=250, blank=True, null=True)
    celularRepresentante = models.CharField(max_length=250, blank=True, null=True)
    whatsappRepresentante = models.CharField(max_length=250, blank=True, null=True)
    correoRepresentante = models.CharField(max_length=250, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    state = models.SmallIntegerField(default=1)


class ValidarCuenta(models.Model):
    _id = models.ObjectIdField()
    codigo = models.CharField(max_length=200, null=False)
    user_id = models.CharField(max_length=250, blank=False, null=False)  # Relacion usuario

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    state = models.SmallIntegerField(default=1)
