from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.conf import settings
from django import forms
from django.utils.html import format_html
# Create your models here.
from smart_selects.db_fields import ChainedForeignKey
from solo.models import SingletonModel

from django.core.validators import RegexValidator
from django.forms import TextInput


from CONFIGURACION.models import *
from TECNOLOGIAS.models import *



class TipoDeInstitucionProductiva(models.Model):
    class Meta:
        verbose_name = 'Tipo De Institución Productiva'
        verbose_name_plural = 'Tipos De Instituciones Productivas'
    nombre = models.CharField(max_length=255)
    def __str__(self):
        return self.nombre

class TipoDeProducto(models.Model):
    class Meta:
        verbose_name = 'Tipo De Producto'
        verbose_name_plural = 'Tipos De Productos'
    nombre = models.CharField(max_length=255)
    def __str__(self):
        return self.nombre



class InstitucionProductiva(models.Model):
    class Meta:
        verbose_name = 'Institución Productiva'
        verbose_name_plural = 'Instituciones Productivas'

    Nombre = models.CharField(max_length=255, unique=True)
    NombreAbreviado  = models.CharField(max_length=255, unique=True,verbose_name="Abreviado")
    Imagen = models.ImageField(upload_to='InstitucionProductiva',blank=True,null=True)
    Contacto = models.CharField(max_length=255)
    Telefono = models.CharField(max_length=255)
    Correo = models.EmailField(max_length=255)
    provincia = models.ForeignKey(Provincia, on_delete=models.CASCADE)
    municipio = ChainedForeignKey(
        Municipio,
        chained_field="provincia",
        chained_model_field="provincia",
        show_all=False,
        auto_choose=True,
        sort=True, on_delete=models.CASCADE)
    Direccion = models.CharField(max_length=255,verbose_name="Dirección")
    tipoDeInstitucionProductiva = models.ForeignKey(TipoDeInstitucionProductiva
                                                    , on_delete=models.CASCADE
                                                    ,verbose_name="Tipo"
                                                    )
    capacidadDeRefrigeracion = models.FloatField(blank=True,verbose_name="Capacidad de refrigeración")
    descripcion = models.TextField(verbose_name="Descripción",blank=True,null=True)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.Nombre

class Producto(models.Model):
    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
    nombre = models.CharField(max_length=255)
    tipoDeProducto = models.ForeignKey(TipoDeProducto
                                       , on_delete=models.CASCADE
                                       ,verbose_name="Tipo")
    institucionProductiva = models.ForeignKey(InstitucionProductiva, on_delete=models.CASCADE)
    Imagen = models.ImageField(upload_to='Productos', blank=True, null=True)
    descripcion = models.TextField(verbose_name="Descripción", blank=True, null=True)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.nombre
