from django.db import models

def upload_path(instance, filname):
    return '/'.join(['MDM/imgClientes', str(instance.id) +"_" + filname])

# Create your models here.
class Clientes(models.Model):
    tipoCliente = models.CharField(max_length=150,null=True)
    cedula = models.CharField(max_length=10,null=True,unique=True)
    nombreCompleto = models.CharField(max_length=255,null=True)
    nombres = models.CharField(max_length=150,null=True)
    apellidos = models.CharField(max_length=150,null=True)
    genero= models.CharField(max_length=150,null=True)
    nacionalidad= models.CharField(max_length=150,null=True)
    fechaNacimiento = models.DateField(null=True)
    edad = models.SmallIntegerField(null=True)
    paisNacimiento= models.CharField(max_length=150,null=True)
    provinciaNacimiento= models.CharField(max_length=150,null=True)
    ciudadNacimiento= models.CharField(max_length=150,null=True)
    estadoCivil= models.CharField(max_length=150,null=True)
    paisResidencia= models.CharField(max_length=150,null=True)
    provinciaResidencia= models.CharField(max_length=150,null=True)
    ciudadResidencia= models.CharField(max_length=150,null=True)
    nivelEstudios= models.CharField(max_length=150,null=True)
    profesion= models.CharField(max_length=150,null=True)
    lugarTrabajo = models.CharField(max_length=150,null=True)
    paisTrabajo= models.CharField(max_length=150,null=True)
    provinciaTrabajo= models.CharField(max_length=150,null=True)
    ciudadTrabajo= models.CharField(max_length=150,null=True)
    mesesUltimoTrabajo = models.PositiveIntegerField(null=True)
    mesesTotalTrabajo = models.PositiveIntegerField (null=True)
    ingresosPromedioMensual = models.FloatField(null=True)
    gastosPromedioMensual = models.FloatField(null=True)
    imagen=models.ImageField(blank=True,null=True,upload_to=upload_path)
    estado=models.CharField(max_length=200,default="Inactivo")
    correo= models.EmailField(max_length=150,null=True)
    telefono= models.CharField(max_length=20,null=True)
    # Id de la empresa que se inicia sesion
    empresa_id = models.CharField(max_length=255,null=False, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    state = models.SmallIntegerField(default=1)

    def save(self, *args, **kwargs):
        # self.tipo = self.tipo.upper()
        return super(Clientes, self).save(*args, **kwargs)

    # def __str__(self):
    #     return '{}'.format(self.nombres)

class DatosFisicosClientes(models.Model):
    cliente= models.ForeignKey(Clientes, null=True, blank=True, on_delete=models.DO_NOTHING)  # Relacion Con el cliente
    tipoDireccion= models.CharField(max_length=150,null=True,blank=True)
    pais= models.CharField(max_length=150,null=True,blank=True)
    provincia= models.CharField(max_length=150,null=True,blank=True)
    ciudad= models.CharField(max_length=150,null=True,blank=True)
    callePrincipal = models.CharField(max_length=150,null=True,blank=True)
    numero = models.CharField(max_length=20,null=True,blank=True)
    calleSecundaria = models.CharField(max_length=150,null=True,blank=True)
    edificio = models.CharField(max_length=150,null=True,blank=True)
    piso = models.CharField(max_length=150,null=True,blank=True)
    oficina = models.CharField(max_length=150,null=True,blank=True)
    referencia = models.CharField(max_length=150,null=True,blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    state = models.SmallIntegerField(default=1)

    def save(self, *args, **kwargs):
        # self.tipo = self.tipo.upper()
        return super(DatosFisicosClientes, self).save(*args, **kwargs)

    def __str__(self):
        return '{}'.format(self.nombres)

class DatosVirtualesClientes(models.Model):
    cliente= models.ForeignKey(Clientes, null=True, blank=True, on_delete=models.DO_NOTHING)  # Relacion Con el cliente
    tipoContacto= models.CharField(max_length=150,null=True,blank=True)
    informacion = models.TextField(max_length=150,null=True,blank=True)
    icono = models.CharField(max_length=150,null=True,blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    state = models.SmallIntegerField(default=1)

    def save(self, *args, **kwargs):
        # self.tipo = self.tipo.upper()
        return super(DatosVirtualesClientes, self).save(*args, **kwargs)

    # def __str__(self):
    #     return '{}'.format(self.nombres)

class Parientes(models.Model):
    cliente= models.ForeignKey(Clientes, null=True, blank=True, on_delete=models.DO_NOTHING)  # Relacion Con el cliente
    tipoPariente= models.CharField(max_length=150,null=True,blank=True)
    cedula = models.CharField(max_length=10,null=True,unique=True)
    nombres = models.CharField(max_length=150,null=True,blank=True)
    apellidos = models.CharField(max_length=150,null=True,blank=True)
    fechaMatrimonio = models.DateField(null=True,blank=True)
    lugarMatrimonio = models.CharField(max_length=150,null=True,blank=True)
    genero= models.CharField(max_length=150,null=True,blank=True)
    nacionalidad= models.CharField(max_length=150,null=True,blank=True)
    fechaNacimiento = models.DateField(null=True,blank=True)
    edad = models.PositiveSmallIntegerField(null=True,blank=True)
    paisNacimiento= models.CharField(max_length=150,null=True,blank=True)
    provinciaNacimiento= models.CharField(max_length=150,null=True,blank=True)
    ciudadNacimiento= models.CharField(max_length=150,null=True,blank=True)
    estadoCivil= models.CharField(max_length=150,null=True,blank=True)
    paisResidencia= models.CharField(max_length=150,null=True,blank=True)
    provinciaResidencia= models.CharField(max_length=150,null=True,blank=True)
    ciudadResidencia= models.CharField(max_length=150,null=True,blank=True)
    callePrincipal = models.CharField(max_length=150,null=True,blank=True)
    numero = models.CharField(max_length=20,null=True,blank=True)
    calleSecundaria = models.CharField(max_length=150,null=True,blank=True)
    edificio = models.CharField(max_length=150,null=True,blank=True)
    piso = models.CharField(max_length=150,null=True,blank=True)
    departamento = models.CharField(max_length=150,null=True,blank=True)
    telefonoDomicilio = models.CharField(max_length=15,null=True,blank=True)
    telefonoOficina = models.CharField(max_length=15,null=True,blank=True)
    celularPersonal = models.CharField(max_length=15,null=True,blank=True)
    celularOficina = models.CharField(max_length=15,null=True,blank=True)
    whatsappPersonal = models.CharField(max_length=150,null=True,blank=True)
    whatsappSecundario = models.CharField(max_length=150,null=True,blank=True)
    correoPersonal = models.EmailField(max_length=150,null=True,blank=True)
    correoTrabajo = models.EmailField(max_length=150,null=True,blank=True)
    googlePlus = models.EmailField(max_length=150,null=True,blank=True)
    twitter = models.CharField(max_length=150,null=True,blank=True)
    facebook = models.CharField(max_length=150,null=True,blank=True)
    instagram = models.CharField(max_length=150,null=True,blank=True)
    nivelEstudios= models.CharField(max_length=150,null=True,blank=True)
    profesion= models.CharField(max_length=150,null=True,blank=True)
    lugarTrabajo = models.CharField(max_length=150,null=True,blank=True)
    paisTrabajo= models.CharField(max_length=150,null=True,blank=True)
    provinciaTrabajo= models.CharField(max_length=150,null=True,blank=True)
    ciudadTrabajo= models.CharField(max_length=150,null=True,blank=True)
    mesesUltimoTrabajo = models.PositiveIntegerField(null=True,blank=True)
    mesesTotalTrabajo = models.PositiveIntegerField(null=True,blank=True)
    ingresosPromedioMensual = models.FloatField(null=True,blank=True)
    gastosPromedioMensual = models.FloatField(null=True,blank=True)
    estado=models.CharField(max_length=200,default="Inactivo")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    state = models.SmallIntegerField(default=1)

    def save(self, *args, **kwargs):
        # self.tipo = self.tipo.upper()
        return super(Parientes, self).save(*args, **kwargs)

    def __str__(self):
        return '{}'.format(self.nombres)