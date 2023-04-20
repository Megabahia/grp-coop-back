# Generated by Django 3.1.7 on 2021-12-10 16:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('corp_empresas', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='empresas',
            old_name='local',
            new_name='direccion',
        ),
        migrations.RenameField(
            model_name='empresas',
            old_name='nombre',
            new_name='nombreComercial',
        ),
        migrations.RenameField(
            model_name='empresas',
            old_name='telefono',
            new_name='telefono1',
        ),
        migrations.AddField(
            model_name='empresas',
            name='correo',
            field=models.EmailField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='empresas',
            name='nombreEmpresa',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='empresas',
            name='pais',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='empresas',
            name='telefono2',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='empresas',
            name='tipoCategoria',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='empresas',
            name='tipoEmpresa',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='empresas',
            name='ruc',
            field=models.CharField(blank=True, max_length=13, null=True),
        ),
    ]