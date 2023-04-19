from djongo import models

# Create your models here.
class TipoUsuario(models.Model):
    _id = models.ObjectIdField()
    nombre = models.CharField(max_length=200,null=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    state = models.SmallIntegerField(default=1)