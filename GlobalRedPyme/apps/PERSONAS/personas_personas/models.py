import jsonfield
from djongo import models


def upload_path(instance, filname):
    return '/'.join(['PERSONAS/imgPersonas', str(instance._id) + "_" + filname])


# Create your models here.
class Personas(models.Model):
    _id = models.ObjectIdField()
    identificacion = models.TextField()
    nombres = models.TextField()
    apellidos = models.TextField()
    nombresCompleto = models.TextField()
    genero = models.TextField()
    fechaNacimiento = models.TextField()
    edad = models.TextField()
    ciudad = models.TextField()
    provincia = models.TextField()
    pais = models.TextField()
    direccion = models.TextField()
    email = models.TextField()
    emailAdicional = models.TextField()
    telefono = models.TextField()
    whatsapp = models.TextField()
    facebook = models.TextField()
    instagram = models.TextField()
    twitter = models.TextField()
    tiktok = models.TextField()
    youtube = models.TextField()
    imagen = models.FileField(blank=True, null=True, upload_to=upload_path)
    user_id = models.CharField(max_length=250, blank=False, null=False)  # Relacion usuario
    empresaInfo = models.TextField()
    datosPyme = models.TextField()
    estadoCivil = models.TextField()
    cedulaRepresentante = models.TextField()
    direccionRepresentante = models.TextField()
    celularRepresentante = models.TextField()
    whatsappRepresentante = models.TextField()
    correoRepresentante = models.TextField()
    autorizacion = models.TextField()

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
