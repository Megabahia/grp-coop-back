from djongo import models
from apps.PERSONAS.personas_personas.models import Personas


# Create your models here.
class HistorialLaboral(models.Model):
    _id = models.ObjectIdField()
    fechaInicio = models.DateField(null=True, blank=True)
    empresa = models.CharField(max_length=200,null=True, blank=True)
    tiempoTrabajo = models.SmallIntegerField(null=True, blank=True)
    cargoActual = models.CharField(max_length=200,null=True, blank=True)
    estado = models.CharField(max_length=200,null=True, blank=True)
    profesion = models.CharField(max_length=255,null=True, blank=True)
    user_id = models.CharField(max_length=255,null=True,blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    state = models.SmallIntegerField(default=1)