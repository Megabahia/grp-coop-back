import jsonfield
from djongo import models


# Create your models here.
class Catalogo(models.Model):
    _id = models.ObjectIdField()
    idPadre = models.ForeignKey('self', null=True, blank=True, on_delete=models.DO_NOTHING)  # Relacion Padre
    nombre = models.CharField(max_length=255, null=True)
    tipo = models.CharField(max_length=255, null=False)
    tipoVariable = models.CharField(max_length=255, null=False)
    valor = models.CharField(max_length=255, null=False)
    descripcion = models.CharField(max_length=255, null=True)
    config = jsonfield.JSONField()
    minimo = models.IntegerField(null=True, blank=True)
    maximo = models.IntegerField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    state = models.SmallIntegerField(default=1)

    def save(self, *args, **kwargs):
        self.tipo = self.tipo.upper()
        return super(Catalogo, self).save(*args, **kwargs)

    def __str__(self):
        return '{}'.format(self.nombre)
