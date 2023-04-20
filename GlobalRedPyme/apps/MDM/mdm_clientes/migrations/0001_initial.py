# Generated by Django 3.1.7 on 2022-02-17 15:43

import apps.MDM.mdm_clientes.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Clientes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipoCliente', models.CharField(max_length=150, null=True)),
                ('cedula', models.CharField(max_length=10, null=True, unique=True)),
                ('nombreCompleto', models.CharField(max_length=255, null=True)),
                ('nombres', models.CharField(max_length=150, null=True)),
                ('apellidos', models.CharField(max_length=150, null=True)),
                ('genero', models.CharField(max_length=150, null=True)),
                ('nacionalidad', models.CharField(max_length=150, null=True)),
                ('fechaNacimiento', models.DateField(null=True)),
                ('edad', models.SmallIntegerField(null=True)),
                ('paisNacimiento', models.CharField(max_length=150, null=True)),
                ('provinciaNacimiento', models.CharField(max_length=150, null=True)),
                ('ciudadNacimiento', models.CharField(max_length=150, null=True)),
                ('estadoCivil', models.CharField(max_length=150, null=True)),
                ('paisResidencia', models.CharField(max_length=150, null=True)),
                ('provinciaResidencia', models.CharField(max_length=150, null=True)),
                ('ciudadResidencia', models.CharField(max_length=150, null=True)),
                ('nivelEstudios', models.CharField(max_length=150, null=True)),
                ('profesion', models.CharField(max_length=150, null=True)),
                ('lugarTrabajo', models.CharField(max_length=150, null=True)),
                ('paisTrabajo', models.CharField(max_length=150, null=True)),
                ('provinciaTrabajo', models.CharField(max_length=150, null=True)),
                ('ciudadTrabajo', models.CharField(max_length=150, null=True)),
                ('mesesUltimoTrabajo', models.PositiveIntegerField(null=True)),
                ('mesesTotalTrabajo', models.PositiveIntegerField(null=True)),
                ('ingresosPromedioMensual', models.FloatField(null=True)),
                ('gastosPromedioMensual', models.FloatField(null=True)),
                ('imagen', models.ImageField(blank=True, null=True, upload_to=apps.MDM.mdm_clientes.models.upload_path)),
                ('estado', models.CharField(default='Inactivo', max_length=200)),
                ('correo', models.EmailField(max_length=150, null=True)),
                ('telefono', models.CharField(max_length=20, null=True)),
                ('empresa_id', models.CharField(blank=True, max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(null=True)),
                ('state', models.SmallIntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='Parientes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipoPariente', models.CharField(blank=True, max_length=150, null=True)),
                ('cedula', models.CharField(max_length=10, null=True, unique=True)),
                ('nombres', models.CharField(blank=True, max_length=150, null=True)),
                ('apellidos', models.CharField(blank=True, max_length=150, null=True)),
                ('fechaMatrimonio', models.DateField(blank=True, null=True)),
                ('lugarMatrimonio', models.CharField(blank=True, max_length=150, null=True)),
                ('genero', models.CharField(blank=True, max_length=150, null=True)),
                ('nacionalidad', models.CharField(blank=True, max_length=150, null=True)),
                ('fechaNacimiento', models.DateField(blank=True, null=True)),
                ('edad', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('paisNacimiento', models.CharField(blank=True, max_length=150, null=True)),
                ('provinciaNacimiento', models.CharField(blank=True, max_length=150, null=True)),
                ('ciudadNacimiento', models.CharField(blank=True, max_length=150, null=True)),
                ('estadoCivil', models.CharField(blank=True, max_length=150, null=True)),
                ('paisResidencia', models.CharField(blank=True, max_length=150, null=True)),
                ('provinciaResidencia', models.CharField(blank=True, max_length=150, null=True)),
                ('ciudadResidencia', models.CharField(blank=True, max_length=150, null=True)),
                ('callePrincipal', models.CharField(blank=True, max_length=150, null=True)),
                ('numero', models.CharField(blank=True, max_length=20, null=True)),
                ('calleSecundaria', models.CharField(blank=True, max_length=150, null=True)),
                ('edificio', models.CharField(blank=True, max_length=150, null=True)),
                ('piso', models.CharField(blank=True, max_length=150, null=True)),
                ('departamento', models.CharField(blank=True, max_length=150, null=True)),
                ('telefonoDomicilio', models.CharField(blank=True, max_length=15, null=True)),
                ('telefonoOficina', models.CharField(blank=True, max_length=15, null=True)),
                ('celularPersonal', models.CharField(blank=True, max_length=15, null=True)),
                ('celularOficina', models.CharField(blank=True, max_length=15, null=True)),
                ('whatsappPersonal', models.CharField(blank=True, max_length=150, null=True)),
                ('whatsappSecundario', models.CharField(blank=True, max_length=150, null=True)),
                ('correoPersonal', models.EmailField(blank=True, max_length=150, null=True)),
                ('correoTrabajo', models.EmailField(blank=True, max_length=150, null=True)),
                ('googlePlus', models.EmailField(blank=True, max_length=150, null=True)),
                ('twitter', models.CharField(blank=True, max_length=150, null=True)),
                ('facebook', models.CharField(blank=True, max_length=150, null=True)),
                ('instagram', models.CharField(blank=True, max_length=150, null=True)),
                ('nivelEstudios', models.CharField(blank=True, max_length=150, null=True)),
                ('profesion', models.CharField(blank=True, max_length=150, null=True)),
                ('lugarTrabajo', models.CharField(blank=True, max_length=150, null=True)),
                ('paisTrabajo', models.CharField(blank=True, max_length=150, null=True)),
                ('provinciaTrabajo', models.CharField(blank=True, max_length=150, null=True)),
                ('ciudadTrabajo', models.CharField(blank=True, max_length=150, null=True)),
                ('mesesUltimoTrabajo', models.PositiveIntegerField(blank=True, null=True)),
                ('mesesTotalTrabajo', models.PositiveIntegerField(blank=True, null=True)),
                ('ingresosPromedioMensual', models.FloatField(blank=True, null=True)),
                ('gastosPromedioMensual', models.FloatField(blank=True, null=True)),
                ('estado', models.CharField(default='Inactivo', max_length=200)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(null=True)),
                ('state', models.SmallIntegerField(default=1)),
                ('cliente', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='mdm_clientes.clientes')),
            ],
        ),
        migrations.CreateModel(
            name='DatosVirtualesClientes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipoContacto', models.CharField(blank=True, max_length=150, null=True)),
                ('informacion', models.TextField(blank=True, max_length=150, null=True)),
                ('icono', models.CharField(blank=True, max_length=150, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(null=True)),
                ('state', models.SmallIntegerField(default=1)),
                ('cliente', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='mdm_clientes.clientes')),
            ],
        ),
        migrations.CreateModel(
            name='DatosFisicosClientes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipoDireccion', models.CharField(blank=True, max_length=150, null=True)),
                ('pais', models.CharField(blank=True, max_length=150, null=True)),
                ('provincia', models.CharField(blank=True, max_length=150, null=True)),
                ('ciudad', models.CharField(blank=True, max_length=150, null=True)),
                ('callePrincipal', models.CharField(blank=True, max_length=150, null=True)),
                ('numero', models.CharField(blank=True, max_length=20, null=True)),
                ('calleSecundaria', models.CharField(blank=True, max_length=150, null=True)),
                ('edificio', models.CharField(blank=True, max_length=150, null=True)),
                ('piso', models.CharField(blank=True, max_length=150, null=True)),
                ('oficina', models.CharField(blank=True, max_length=150, null=True)),
                ('referencia', models.CharField(blank=True, max_length=150, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(null=True)),
                ('state', models.SmallIntegerField(default=1)),
                ('cliente', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='mdm_clientes.clientes')),
            ],
        ),
    ]