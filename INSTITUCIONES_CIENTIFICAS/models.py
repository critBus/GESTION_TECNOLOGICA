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
        app_label = 'INSTITUCIONES_CIENTIFICAS'
    nombre = models.CharField(max_length=255,unique=True)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.nombre

class Especie(models.Model):
    class Meta:
        verbose_name = 'Especie'
        verbose_name_plural = 'Especies'
        app_label = 'INSTITUCIONES_CIENTIFICAS'
        ordering=('nombreComun',)
    nombreCientifico = models.CharField(max_length=255,unique=True,verbose_name="Nombre Científico")
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
        app_label='INSTITUCIONES_CIENTIFICAS'
    nombre = models.CharField(max_length=255,unique=True)
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




#--------------------------

class TipoDeInstitucionCientifica(models.Model):
    class Meta:
        verbose_name = 'Tipo De Institución Científica'
        verbose_name_plural = 'Tipos De Instituciones Científicas'
    nombre = models.CharField(max_length=255,unique=True)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.nombre



# from django.contrib.gis.db import models
class InstitucionCientifica(models.Model):
    class Meta:
        verbose_name = 'Institución Científica'
        verbose_name_plural = 'Instituciones Científicas'

    # location=models.PointField(blank=True,null=True)
    Nombre = models.CharField(max_length=255, unique=True)
    NombreAbreviado  = models.CharField(max_length=255, unique=True,verbose_name="Abreviado")
    Imagen = models.ImageField(upload_to='InstitucionCientifica',blank=True,null=True)
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
        sort=True, on_delete=models.CASCADE

    )
    Direccion = models.CharField(max_length=255,verbose_name="Dirección")
    tipoDeInstitucionCientifica = models.ForeignKey(TipoDeInstitucionCientifica
                                                    , on_delete=models.CASCADE
                                                    ,verbose_name="Tipo")

    tecnologias = models.ManyToManyField(Tecnologia)#,verbose_name="Tecnologias"
    descripcion = models.TextField(verbose_name="Descripción", blank=True, null=True)
    created=models.DateTimeField(auto_now_add=True)
    modified=models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.Nombre



class InstitucionCientificaResource(resources.ModelResource):
    tecnologias=Field()
    NombreAbreviado=Field(
        column_name='Nombre Abreviado'
        , attribute='NombreAbreviado'
    )
    tipoDeInstitucionCientifica=Field(
        column_name='Tipo'
        , attribute='tipoDeInstitucionCientifica'
    )

    provincia=Field()
    class Meta:
        model = InstitucionCientifica
        fields = ('Nombre','Contacto','Telefono','Correo','municipio','Direccion')
        export_order = ('Nombre', 'NombreAbreviado','Contacto','Telefono','Correo','provincia','municipio','Direccion','tipoDeInstitucionCientifica')

    @staticmethod
    @retornarBienDatoExportar
    def dehydrate_tecnologias(instance):
        if instance.tecnologias is not None:
            return "\n".join([z.nombre for z in instance.tecnologias.all()])
        return ""

    @staticmethod
    @retornarBienDatoExportar
    def dehydrate_provincia(instance):
        if instance.provincia is not None:
            return instance.provincia.nombre
        return ""





