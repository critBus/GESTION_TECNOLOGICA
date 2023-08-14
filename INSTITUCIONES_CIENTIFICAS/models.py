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




# Register your models here.



class TipoDeInstitucionCientifica(models.Model):
    class Meta:
        verbose_name = 'Tipo De Institución Científica'
        verbose_name_plural = 'Tipos De Instituciones Científicas'
    nombre = models.CharField(max_length=255)
    def __str__(self):
        return self.nombre




class InstitucionCientifica(models.Model):
    class Meta:
        verbose_name = 'Institución Científica'
        verbose_name_plural = 'Instituciones Científicas'


    Nombre = models.CharField(max_length=255, unique=True)
    NombreAbreviado  = models.CharField(max_length=255, unique=True,verbose_name="Abreviado")
    Imagen = models.ImageField(upload_to='InstitucionCientifica',blank=True,null=True)
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
    tipoDeInstitucionCientifica = models.ForeignKey(TipoDeInstitucionCientifica
                                                    , on_delete=models.CASCADE
                                                    ,verbose_name="Tipo")

    tecnologias = models.ManyToManyField(Tecnologia)
    descripcion = models.TextField(verbose_name="Descripción", blank=True, null=True)
    created=models.DateTimeField(auto_now_add=True)
    modified=models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.Nombre
