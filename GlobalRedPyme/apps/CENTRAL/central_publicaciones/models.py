from djongo import models

def upload_path(instance, filname):
    return '/'.join(['CENTRAL/imgPublicaciones', str(instance._id) + "_" + filname])

from apps.CENTRAL.central_usuarios.models import Usuarios

# Create your models here.
class Publicaciones(models.Model):
    _id = models.ObjectIdField()
    titulo = models.CharField(max_length=200,null=False)
    subtitulo = models.CharField(max_length=200,null=False)
    descripcion = models.TextField(null=False)
    imagen = models.FileField(blank=True,null=True,upload_to=upload_path)
    url = models.TextField(null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    state = models.SmallIntegerField(default=1)

class CompartirPublicaciones(models.Model):
    _id = models.ObjectIdField()
    publicacion = models.ForeignKey(Publicaciones, null=False, on_delete=models.CASCADE)  # Relacion Rol
    user = models.ForeignKey(Usuarios, null=False, on_delete=models.CASCADE)  # Relacion Rol   
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    state = models.SmallIntegerField(default=1)
