from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.conf import settings
from django import forms
from django.utils.html import format_html
# Create your models here.
from smart_selects.db_fields import ChainedForeignKey
from solo.models import SingletonModel

from django.core.exceptions import ValidationError

from django.core.validators import RegexValidator
from django.forms import TextInput
from import_export import resources
from import_export.admin import ExportActionMixin, ImportExportActionModelAdmin
from import_export.widgets import ManyToManyWidget
from import_export.fields import Field
from GESTION_TECNOLOGICA.Utiles.UtilesParaExportar import *

from CONFIGURACION.models import *
from TECNOLOGIAS.models import *



class TipoDeInstitucionProductiva(models.Model):
    class Meta:
        verbose_name = 'Tipo De Institución Productiva'
        verbose_name_plural = 'Tipos De Instituciones Productivas'
    nombre = models.CharField(max_length=255,unique=True)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.nombre

class TipoDeProducto(models.Model):
    class Meta:
        verbose_name = 'Tipo De Producto'
        verbose_name_plural = 'Tipos De Productos'
    nombre = models.CharField(max_length=255,unique=True)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.nombre

VALIDADOR_CAPACIDAD_PRODUCTOS=MinValueValidator(limit_value=1,message="La capacidad de productos debe de ser superior a 1 ")

#from djgeojson.fields import PointField


class Producto(models.Model):
    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
    nombre = models.CharField(max_length=255)
    tipoDeProducto = models.ForeignKey(TipoDeProducto
                                       , on_delete=models.CASCADE
                                       ,verbose_name="Tipo")
    # institucionProductiva = models.ForeignKey(InstitucionProductiva, on_delete=models.CASCADE)
    Imagen = models.ImageField(upload_to='Productos', blank=True, null=True)
    descripcion = models.TextField(verbose_name="Descripción", blank=True, null=True)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.nombre

class InstitucionProductiva(models.Model):
    class Meta:
        verbose_name = 'Institución Productiva'
        verbose_name_plural = 'Instituciones Productivas'

    Nombre = models.CharField(max_length=255, unique=True)
    NombreAbreviado  = models.CharField(max_length=255, unique=True,verbose_name="Abreviado")
    latitud = models.FloatField(verbose_name="Latitud")
    longitud = models.FloatField(verbose_name="Longitud")
    Imagen = models.ImageField(upload_to='InstitucionProductiva',blank=True,null=True)
    Contacto = models.CharField(max_length=255,validators=[VALIDADOR_NOMBRE])
    Telefono = models.CharField(max_length=255,validators=[VALIDADOR_TELEFONO])
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
    capacidadDeProductos=models.IntegerField(default=5
                                             ,validators=[VALIDADOR_CAPACIDAD_PRODUCTOS]
                                             ,verbose_name="Capacidad de Productos")

    TieneAlamacenConRefrigeracion=models.BooleanField(default=False
                                                      ,verbose_name="Tiene Refrigeración")

    productos = models.ManyToManyField(Producto)

    # capacidadDeRefrigeracion = models.FloatField(
    #     verbose_name="Capacidad de refrigeración en KG",blank=True,null=True)
    descripcion = models.TextField(verbose_name="Descripción",blank=True,null=True)



    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    # def clean(self):
    #     if self.TieneAlamacenConRefrigeracion:
    #         if (not self.capacidadDeRefrigeracion) or self.capacidadDeRefrigeracion < 0:
    #             raise ValidationError("La capacidad de refrigeración debe ser superior a 0")

    def __str__(self):
        return self.Nombre


#============================


class InstitucionProductivaResource(resources.ModelResource):
    producto=Field()
    NombreAbreviado=Field(
        column_name='Nombre Abreviado'
        , attribute='NombreAbreviado'
    )
    tipoDeInstitucionProductiva=Field(
        column_name='Tipo'
        , attribute='tipoDeInstitucionProductiva'
    )
    capacidadDeProductos=Field(
        column_name='Capacidad De Productos'
        , attribute='capacidadDeProductos'
    )
    TieneAlamacenConRefrigeracion=Field(
        column_name='Refrigeración'
        , attribute='TieneAlamacenConRefrigeracion'
    )
    provincia=Field()
    class Meta:
        model = InstitucionProductiva
        fields = ('Nombre','Contacto','Telefono','Correo','municipio','Direccion')
        export_order = ('Nombre', 'NombreAbreviado','Contacto','Telefono','Correo','provincia','municipio','Direccion','tipoDeInstitucionProductiva','TieneAlamacenConRefrigeracion','capacidadDeProductos')

    @staticmethod
    @retornarBienDatoExportar
    def dehydrate_producto(instance):
        #if instance.producto_set is not None:
        if instance.productos is not None:
            return "\n".join([z.nombre for z in instance.productos.all()])
        return ""

    @staticmethod
    @retornarBienDatoExportar
    def dehydrate_TieneAlamacenConRefrigeracion(instance):
        if instance.TieneAlamacenConRefrigeracion is not None \
                and instance.TieneAlamacenConRefrigeracion:
            return "Si"
        return "No"
    @staticmethod
    @retornarBienDatoExportar
    def dehydrate_provincia(instance):
        if instance.provincia is not None:
            return instance.provincia.nombre
        return ""




class ProductoResource(resources.ModelResource):
    tipoDeProducto=Field(
        column_name='Tipo'
        , attribute='tipoDeProducto'
    )
    institucionProductiva=Field(
        column_name='Institucón'
        , attribute='institucionProductiva'
    )
    capacidadDeRefrigeracion=Field(
        column_name='Refrigeración'
        , attribute='capacidadDeRefrigeracion'
    )
    class Meta:
        model = Producto
        fields = ('nombre')
        export_order = ('nombre', 'tipoDeProducto','institucionProductiva')

    @staticmethod
    @retornarBienDatoExportar
    def dehydrate_tipoDeProducto(instance):
        if instance.tipoDeProducto is not None:
            return instance.tipoDeProducto.nombre
        return ""

    @staticmethod
    @retornarBienDatoExportar
    def dehydrate_institucionProductiva(instance):
        if instance.institucionProductiva is not None:
            return instance.institucionProductiva.Nombre
        return ""

