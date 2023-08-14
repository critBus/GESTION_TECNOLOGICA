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

from import_export import resources
from import_export.admin import ExportActionMixin, ImportExportActionModelAdmin
from import_export.widgets import ManyToManyWidget
from import_export.fields import Field
from GESTION_TECNOLOGICA.Utiles.UtilesParaExportar import *

# Register your models here.


class TipoDeTecnologia(models.Model):
    class Meta:
        verbose_name = 'Tipo De Tecnología'
        verbose_name_plural = 'Tipos De Tecnologías'
    nombre = models.CharField(max_length=255)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.nombre

class Especie(models.Model):
    class Meta:
        verbose_name = 'Especie'
        verbose_name_plural = 'Especies'
    nombreCientifico = models.CharField(max_length=255,verbose_name="Nombre Científico")
    nombreComun = models.CharField(max_length=255,verbose_name="Nombre Común")
    Imagen = models.ImageField(upload_to='Tecnologias', blank=True, null=True)
    tipoDeEspecie = models.CharField(
        max_length=10,
        choices=[("animal","animal"),("vegetal","vegetal")],
        default="animal",
        verbose_name="Tipo"
    )
    descripcion = models.TextField(verbose_name="Descripción", blank=True, null=True)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    #tecnologias = models.ManyToManyField(Tecnologia)
    def __str__(self):
        return self.nombreComun

class Tecnologia(models.Model):
    class Meta:
        verbose_name = 'Tecnología'
        verbose_name_plural = 'Tecnologías'
    nombre = models.CharField(max_length=255)
    Imagen = models.ImageField(upload_to='Tecnologias',blank=True,null=True)
    accionEsperada = models.CharField(max_length=255, verbose_name="Acción Esperada")
    tipoDeTecnologia = models.ForeignKey(TipoDeTecnologia
                                         , on_delete=models.CASCADE
                                         ,verbose_name="Tipo")
    especies = models.ManyToManyField(Especie, verbose_name="Especies")
    descripcion = models.TextField(verbose_name="Descripción")

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.nombre




class EspecieResource(resources.ModelResource):
    nombreCientifico=Field(
        column_name='Nombre Científico'
        , attribute='nombreCientifico'
    )
    nombreComun=Field(
        column_name='Nombre Común'
        , attribute='nombreComun'
    )

    tipoDeEspecie = Field(
        column_name='Tipo'
        , attribute='tipoDeEspecie'
    )
    class Meta:
        model = Especie
        fields = ()
        export_order = ('nombreCientifico', 'nombreComun','tipoDeEspecie')


class TecnologiaResource(resources.ModelResource):
    especies=Field()
    accionEsperada=Field(
        column_name='Accion Esperada'
        , attribute='accionEsperada'
    )
    tipoDeTecnologia=Field(
        column_name='Tipo'
        , attribute='tipoDeTecnologia'
    )


    class Meta:
        model = Tecnologia
        fields = ('nombre',)
        export_order = ('nombre', 'accionEsperada','tipoDeTecnologia')

    @staticmethod
    @retornarBienDatoExportar
    def dehydrate_especies(instance):
        if instance.especies is not None:
            return "\n".join([z.nombreCientifico for z in instance.especies.all()])
        return ""

