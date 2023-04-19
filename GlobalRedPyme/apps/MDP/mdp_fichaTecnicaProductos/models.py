from django.db import models

from apps.MDP.mdp_productos.models import Productos

# Create your models here.
class FichaTecnicaProductos(models.Model):
    producto= models.ForeignKey(Productos, null=True, blank=True, on_delete=models.DO_NOTHING)  # Relacion Con la categoria
    codigo = models.CharField(max_length=150,null=False)
    nombreAtributo = models.CharField(max_length=255,null=False)
    valor = models.CharField(max_length=150,null=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    state = models.SmallIntegerField(default=1)

    def save(self, *args, **kwargs):
        return super(FichaTecnicaProductos, self).save(*args, **kwargs)

    def __str__(self):
        return '{}'.format(self.nombre)

