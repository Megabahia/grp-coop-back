# Generated by Django 3.1.7 on 2021-12-15 21:09

from django.db import migrations, models
import djongo.models.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Pagos',
            fields=[
                ('_id', djongo.models.fields.ObjectIdField(auto_created=True, primary_key=True, serialize=False)),
                ('codigoCobro', models.CharField(blank=True, max_length=200, null=True)),
                ('duracion', models.DateTimeField(blank=True, null=True)),
                ('monto', models.FloatField(blank=True, null=True)),
                ('user_id', models.CharField(blank=True, max_length=250, null=True)),
                ('empresa_id', models.CharField(blank=True, max_length=250, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(null=True)),
                ('state', models.SmallIntegerField(default=1)),
            ],
        ),
    ]