from djongo import models
from apps.CENTRAL.central_usuarios.models import Usuarios


# Create your models here.
class InfoUsuarios(models.Model):
    _id = models.ObjectIdField()
    nombres = models.CharField(max_length=200,null=True, blank=True)
    apellidos = models.CharField(max_length=200,null=True, blank=True)
    telefono = models.CharField(max_length=200,null=True, blank=True)
    whatsapp = models.CharField(max_length=200,null=True, blank=True)
    cargo = models.CharField(max_length=200,null=True, blank=True)
    fechaNacimiento = models.DateField(null=True, blank=True)
    genero = models.CharField(max_length=255,null=True, blank=True)
    estado = models.CharField(default="Activo",max_length=200,null=True, blank=True)
    usuario = models.ForeignKey(Usuarios, null=False, on_delete=models.CASCADE)  # Relacion Rol    

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    state = models.SmallIntegerField(default=1)