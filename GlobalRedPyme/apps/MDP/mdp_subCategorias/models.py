from django.db import models

from ..mdp_categorias.models import Categorias


# Mundo: bigpuntos
# Portales: corp
# Esta clase sirve para relacionar la tabla subcategoria de la base datos mdp
class SubCategorias(models.Model):
    categoria = models.ForeignKey(Categorias, null=True, blank=True,
                                  on_delete=models.DO_NOTHING)  # Relacion Con la categoria
    # categoriaPadre = models.CharField(max_length=150,null=False)
    nombre = models.CharField(max_length=150, null=False)
    codigoSubCategoria = models.CharField(max_length=255, null=False)
    descripcion = models.TextField(null=True)
    estado = models.CharField(max_length=150, null=False, default="Inactivo")
    # Id de la empresa que se inicia sesion
    empresa_id = models.CharField(max_length=255, null=False, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    state = models.SmallIntegerField(default=1)
