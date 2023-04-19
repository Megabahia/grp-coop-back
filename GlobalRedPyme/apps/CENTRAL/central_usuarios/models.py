from djongo import models
from django.contrib.auth.models import AbstractBaseUser, UserManager
from apps.CENTRAL.central_tipoUsuarios.models import TipoUsuario

# Create your models here.


class Usuarios(AbstractBaseUser):
    _id = models.ObjectIdField()
    email = models.CharField(max_length=250,blank=True, null=True, unique=True)
    estado = models.CharField(max_length=200,blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True,auto_now_add=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    state = models.SmallIntegerField(default=1)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    objects = UserManager()

    tipoUsuario = models.ForeignKey(TipoUsuario, null=True, on_delete=models.CASCADE)  # Relacion Tipo usuario


class UsuariosEmpresas(models.Model):
    _id = models.ObjectIdField()
    empresa_id = models.TextField(null=True, blank=True)
    usuario = models.ForeignKey(Usuarios, null=True, on_delete=models.CASCADE)  # Relacion Tipo usuario

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    state = models.SmallIntegerField(default=1)
    