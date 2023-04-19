from djongo import models
from apps.CENTRAL.central_roles.models import Roles

# Create your models here.
class Acciones(models.Model):
    _id = models.ObjectIdField()
    codigo = models.CharField(max_length=150,null=False)
    nombre = models.CharField(max_length=200,null=False)
    link = models.CharField(max_length=150,null=True)
    idAccionPadre= models.ForeignKey('self', null=True, blank=True, on_delete=models.DO_NOTHING)  # Relacion Padre
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    state = models.SmallIntegerField(default=1)

    def __str__(self):
        return '{}'.format(self.nombre)

class AccionesPermitidas(models.Model):
    _id = models.ObjectIdField()
    idAccion= models.ForeignKey(Acciones, null=False, on_delete=models.DO_NOTHING)  # Relacion Con Acciones
    url = models.CharField(max_length=150,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    state = models.SmallIntegerField(default=1)

    def __str__(self):
        return '{}'.format(self.url)

class AccionesPorRol(models.Model):
    _id = models.ObjectIdField()
    idAccion= models.ForeignKey(Acciones, null=False, on_delete=models.CASCADE)  # Relacion Con Acciones
    idRol= models.ForeignKey(Roles, null=False, on_delete=models.CASCADE)  # Relacion Con Rol
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    state = models.SmallIntegerField(default=0)


