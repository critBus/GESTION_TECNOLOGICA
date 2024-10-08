# Generated by Django 4.2 on 2023-08-21 17:06

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import smart_selects.db_fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('CONFIGURACION', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='InstitucionProductiva',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Nombre', models.CharField(max_length=255, unique=True)),
                ('NombreAbreviado', models.CharField(max_length=255, unique=True, verbose_name='Abreviado')),
                ('longitud', models.FloatField(verbose_name='Longitud')),
                ('latitud', models.FloatField(verbose_name='Latitud')),
                ('Imagen', models.ImageField(blank=True, null=True, upload_to='InstitucionProductiva')),
                ('Contacto', models.CharField(max_length=255, validators=[django.core.validators.RegexValidator(message='Nombre incorrecto', regex='^[a-zA-ZáéíóúÁÉÍÓÚÑñ]+(?:\\s+[a-zA-ZáéíóúÁÉÍÓÚÑñ]+){1,5}$')])),
                ('Telefono', models.CharField(max_length=255, validators=[django.core.validators.RegexValidator(message='Teléfono incorrecto', regex='^([+]?53)?\\d{8}$')])),
                ('Correo', models.EmailField(max_length=255)),
                ('Direccion', models.CharField(max_length=255, verbose_name='Dirección')),
                ('capacidadDeProductos', models.IntegerField(default=5, validators=[django.core.validators.MinValueValidator(limit_value=1, message='La capacidad de productos debe de ser superior a 1 ')], verbose_name='Capacidad de Productos')),
                ('TieneAlamacenConRefrigeracion', models.BooleanField(default=False, verbose_name='Tiene Refrigeración')),
                ('capacidadDeRefrigeracion', models.FloatField(blank=True, null=True, verbose_name='Capacidad de refrigeración en KG')),
                ('descripcion', models.TextField(blank=True, null=True, verbose_name='Descripción')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('municipio', smart_selects.db_fields.ChainedForeignKey(auto_choose=True, chained_field='provincia', chained_model_field='provincia', on_delete=django.db.models.deletion.CASCADE, to='CONFIGURACION.municipio')),
                ('provincia', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='CONFIGURACION.provincia')),
            ],
            options={
                'verbose_name': 'Institución Productiva',
                'verbose_name_plural': 'Instituciones Productivas',
            },
        ),
        migrations.CreateModel(
            name='TipoDeInstitucionProductiva',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255, unique=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Tipo De Institución Productiva',
                'verbose_name_plural': 'Tipos De Instituciones Productivas',
            },
        ),
        migrations.CreateModel(
            name='TipoDeProducto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255, unique=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Tipo De Producto',
                'verbose_name_plural': 'Tipos De Productos',
            },
        ),
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255)),
                ('Imagen', models.ImageField(blank=True, null=True, upload_to='Productos')),
                ('descripcion', models.TextField(blank=True, null=True, verbose_name='Descripción')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('institucionProductiva', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='INSTITUCIONES_PRODUCTIVAS.institucionproductiva')),
                ('tipoDeProducto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='INSTITUCIONES_PRODUCTIVAS.tipodeproducto', verbose_name='Tipo')),
            ],
            options={
                'verbose_name': 'Producto',
                'verbose_name_plural': 'Productos',
            },
        ),
        migrations.AddField(
            model_name='institucionproductiva',
            name='tipoDeInstitucionProductiva',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='INSTITUCIONES_PRODUCTIVAS.tipodeinstitucionproductiva', verbose_name='Tipo'),
        ),
    ]
