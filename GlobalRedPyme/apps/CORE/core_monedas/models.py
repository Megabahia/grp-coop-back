from djongo import models


# Nube: coop
# Portales: Center, Personas, Corp, IFIS, Credit
# La clase se conecta con la tabla de monedas de la base datos core
class Monedas(models.Model):
    # esta clase se usa para las opciones del campo tipo
    class TipoEnum(models.TextChoices):
        SUPERMONEDAS = 'Supermonedas'
        CREDITO = 'Credito'
        PAGOS = 'Pagos'
        COBROS = 'Cobros'
        DESCUENTOS = 'Descuentos'
        ACUMULACION = 'Acumulación'
        COMSUMO = 'Consumo'
        OTRO = 'Otro'

    # esta clase se crea para las opciones del campo estado
    class EstadoEnum(models.TextChoices):
        APROBADO = 'aprobado'
        RECHAZADO = 'rechazado'
        CANDELADO = 'candelado'
        PENDIENTE = 'pendiente'

    _id = models.ObjectIdField()
    user_id = models.CharField(max_length=200, null=True, blank=True)
    identificacion = models.CharField(max_length=200, null=True, blank=True)
    nombres = models.CharField(max_length=200, null=True, blank=True)
    apellidos = models.CharField(max_length=200, null=True, blank=True)
    email = models.CharField(max_length=200, null=True, blank=True)
    autorizador_id = models.CharField(max_length=200, null=True, blank=True)
    empresa_id = models.CharField(max_length=255, null=True, blank=True)
    tipo = models.CharField(max_length=255, choices=TipoEnum.choices, default=TipoEnum.OTRO)
    estado = models.CharField(max_length=255, choices=EstadoEnum.choices, default=EstadoEnum.PENDIENTE)
    credito = models.IntegerField(default=0)
    debito = models.IntegerField(default=0)
    saldo = models.IntegerField(default=0)
    descripcion = models.CharField(max_length=255, null=True, blank=True)
    fechaVigencia = models.DateField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    state = models.SmallIntegerField(default=1)
