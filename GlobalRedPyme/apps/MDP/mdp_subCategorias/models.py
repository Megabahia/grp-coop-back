from django.db import models

from apps.MDP.mdp_categorias.models import Categorias

# Create your models here.
class SubCategorias(models.Model):
    categoria= models.ForeignKey(Categorias, null=True, blank=True, on_delete=models.DO_NOTHING)  # Relacion Con la categoria
    # categoriaPadre = models.CharField(max_length=150,null=False)
    nombre = models.CharField(max_length=150,null=False)
    codigoSubCategoria = models.CharField(max_length=255,null=False)
    descripcion = models.TextField(null=True)
    estado = models.CharField(max_length=150,null=False,default="Inactivo")
    # Id de la empresa que se inicia sesion
    empresa_id = models.CharField(max_length=255,null=False, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    state = models.SmallIntegerField(default=1)

    def save(self, *args, **kwargs):
        return super(SubCategorias, self).save(*args, **kwargs)

    def __str__(self):
        return '{}'.format(self.nombre)