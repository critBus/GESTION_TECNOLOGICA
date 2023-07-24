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



# Create your models here.


#
# class CustomTelefotoWidget(TextInput):
#     def __init__(self, attrs=None):
#         super().__init__(attrs={'pattern': r'^\d{2}-\d{2}-\d{2}-\d{2}$',
#                                 'title': 'El formato debe ser ##-##-##-##'},
#                          validators=[RegexValidator(r'^\d{2}-\d{2}-\d{2}-\d{2}$',
#                                                     message='El formato debe ser ##-##-##-##')])
#
#     def format_value(self, value):
#         if value:
#             return '{}-{}-{}-{}'.format(value[:2], value[2:4], value[4:6], value[6:])
#         return ''

#
# class ConfiguracionGeneral(SingletonModel):
#     nombreSitio=models.CharField(max_length=20,verbose_name="Sitio",null=True)
#     ImagenLogo = models.ImageField(upload_to='config')
#     linkFacebook=models.CharField(max_length=255,verbose_name="Link Facebook",null=True)
#     linkTwitter = models.CharField(max_length=255, verbose_name="Link Twitter",null=True)
#     linkYoutube= models.CharField(max_length=255, verbose_name="Link Youtube",null=True)
#     correo=models.EmailField(null=True)
#     telefono=models.CharField(max_length=8,null=True)#, widget=CustomTelefotoWidget
#     direccion=models.CharField(max_length=255,verbose_name="Dirección",null=True)
#     horarios = models.TextField()
#     ImagenBreadcrumbs = models.ImageField(upload_to='config')
#
#
#
#     def __str__(self):
#         return "Configuración General"
#
#     class Meta:
#         verbose_name = "Configuración General"
#
# class PaginaPrincipal(SingletonModel):
#     Titulo = models.CharField(max_length=255 )
#     Descripcion = models.TextField()
#     #Imagen = models.ImageField(upload_to='paginaPrincipal')
#
#     def __str__(self):
#         return "Pagina Principal"
#
#     class Meta:
#         verbose_name = "Pagina Principal"
#
#
#
# class ImagenesFondo_Principal(models.Model):
#     class Meta:
#         verbose_name = 'Imágen Fondo'
#         verbose_name_plural = 'Imágenes Fondo'
#
#     Imagen = models.ImageField(upload_to='ImagenesFondo_Principal')
#     Pagina = models.ForeignKey(PaginaPrincipal, on_delete=models.CASCADE
#                                , related_name="pagina_principal_imagenesFondo")
#
#     def __str__(self):
#         return "Imágen Fondo"
#
# class Informacion_Principal(models.Model):
#     class Meta:
#         verbose_name = 'Información Principal '
#         verbose_name_plural = 'Informaciones Principales'
#     Pagina = models.ForeignKey(PaginaPrincipal, on_delete=models.CASCADE,related_name="pagina_principal_informacion")
#     Titulo = models.CharField(max_length=255)
#     Descripcion = models.TextField()
#     Imagen = models.ImageField(upload_to='Informacion_Principal')
#
#     def __str__(self):
#         return  self.Titulo
#
#
# class TipoDeInstitucion(models.Model):
#     class Meta:
#         verbose_name = 'Tipo De Institución'
#         verbose_name_plural = 'Tipos De Instituciones'
#
#     Tipo = models.CharField(max_length=255,unique=True)
#
#     def __str__(self):
#         return  self.Tipo
#
# class Provincia(models.Model):
#     class Meta:
#         verbose_name = 'Provincia'
#         verbose_name_plural = 'Provincias'
#
#     nombre = models.CharField(max_length=255)
#     def __str__(self):
#         return self.nombre
#
# class Municipio(models.Model):
#     class Meta:
#         verbose_name = 'Municipio'
#         verbose_name_plural = 'Municipios'
#     nombre = models.CharField(max_length=255)
#     provincia = models.ForeignKey(Provincia, on_delete=models.CASCADE)
#     def __str__(self):
#         return self.nombre


#
# class TipoDeInstitucionCientifica(models.Model):
#     class Meta:
#         verbose_name = 'Tipo De Institución Científica'
#         verbose_name_plural = 'Tipos De Instituciones Científicas'
#     nombre = models.CharField(max_length=255)
#     def __str__(self):
#         return self.nombre
#
# class TipoDeTecnologia(models.Model):
#     class Meta:
#         verbose_name = 'Tipo De Tecnología'
#         verbose_name_plural = 'Tipos De Tecnologías'
#     nombre = models.CharField(max_length=255)
#     def __str__(self):
#         return self.nombre
#
# class Tecnologia(models.Model):
#     class Meta:
#         verbose_name = 'Tecnología'
#         verbose_name_plural = 'Tecnologías'
#     nombre = models.CharField(max_length=255)
#     Imagen = models.ImageField(upload_to='Tecnologias',blank=True,null=True)
#     accionEsperada = models.CharField(max_length=255, verbose_name="Acción Esperada")
#     tipoDeTecnologia = models.ForeignKey(TipoDeTecnologia
#                                          , on_delete=models.CASCADE
#                                          ,verbose_name="Tipo")
#     descripcion = models.TextField(verbose_name="Descripción")
#
#
#     def __str__(self):
#         return self.nombre
#
# class Especie(models.Model):
#     class Meta:
#         verbose_name = 'Especie'
#         verbose_name_plural = 'Especies'
#     nombreCientifico = models.CharField(max_length=255,verbose_name="Nombre Científico")
#     nombreComun = models.CharField(max_length=255,verbose_name="Nombre Común")
#     tipoDeTecnologia = models.CharField(
#         max_length=10,
#         choices=[("animal","animal"),("vegetal","vegetal")],
#         default="animal",
#     )
#
#     tecnologias = models.ManyToManyField(Tecnologia)
#     def __str__(self):
#         return self.nombreComun
#
# class InstitucionCientifica(models.Model):
#     class Meta:
#         verbose_name = 'Institución Científica'
#         verbose_name_plural = 'Instituciones Científicas'
#
#
#     Nombre = models.CharField(max_length=255, unique=True)
#     NombreAbreviado  = models.CharField(max_length=255, unique=True,verbose_name="Abreviado")
#     Imagen = models.ImageField(upload_to='InstitucionCientifica',blank=True,null=True)
#     Contacto = models.CharField(max_length=255)
#     Telefono = models.CharField(max_length=255)
#     Correo = models.EmailField(max_length=255)
#     provincia = models.ForeignKey(Provincia, on_delete=models.CASCADE)
#     municipio = ChainedForeignKey(
#         Municipio,
#         chained_field="provincia",
#         chained_model_field="provincia",
#         show_all=False,
#         auto_choose=True,
#         sort=True, on_delete=models.CASCADE)
#     Direccion = models.CharField(max_length=255,verbose_name="Dirección")
#     tipoDeInstitucionCientifica = models.ForeignKey(TipoDeInstitucionCientifica
#                                                     , on_delete=models.CASCADE
#                                                     ,verbose_name="Tipo")
#
#     tecnologias = models.ManyToManyField(Tecnologia)
#     def __str__(self):
#         return self.Nombre
#
# class TipoDeInstitucionProductiva(models.Model):
#     class Meta:
#         verbose_name = 'Tipo De Institución Productiva'
#         verbose_name_plural = 'Tipos De Instituciones Productivas'
#     nombre = models.CharField(max_length=255)
#     def __str__(self):
#         return self.nombre
#
# class TipoDeProducto(models.Model):
#     class Meta:
#         verbose_name = 'Tipo De Producto'
#         verbose_name_plural = 'Tipos De Productos'
#     nombre = models.CharField(max_length=255)
#     def __str__(self):
#         return self.nombre
#
#
#
# class InstitucionProductiva(models.Model):
#     class Meta:
#         verbose_name = 'Institución Productiva'
#         verbose_name_plural = 'Instituciones Productivas'
#
#     Nombre = models.CharField(max_length=255, unique=True)
#     NombreAbreviado  = models.CharField(max_length=255, unique=True,verbose_name="Abreviado")
#     Imagen = models.ImageField(upload_to='InstitucionProductiva',blank=True,null=True)
#     Contacto = models.CharField(max_length=255)
#     Telefono = models.CharField(max_length=255)
#     Correo = models.EmailField(max_length=255)
#     provincia = models.ForeignKey(Provincia, on_delete=models.CASCADE)
#     municipio = ChainedForeignKey(
#         Municipio,
#         chained_field="provincia",
#         chained_model_field="provincia",
#         show_all=False,
#         auto_choose=True,
#         sort=True, on_delete=models.CASCADE)
#     Direccion = models.CharField(max_length=255,verbose_name="Dirección")
#     tipoDeInstitucionProductiva = models.ForeignKey(TipoDeInstitucionProductiva
#                                                     , on_delete=models.CASCADE
#                                                     ,verbose_name="Tipo"
#                                                     )
#     capacidadDeRefrigeracion = models.FloatField(blank=True,verbose_name="Capacidad de refrigeración")
#
#
#     def __str__(self):
#         return self.Nombre
#
# class Producto(models.Model):
#     class Meta:
#         verbose_name = 'Producto'
#         verbose_name_plural = 'Productos'
#     nombre = models.CharField(max_length=255)
#     tipoDeProducto = models.ForeignKey(TipoDeProducto
#                                        , on_delete=models.CASCADE
#                                        ,verbose_name="Tipo")
#     institucionProductiva = models.ForeignKey(InstitucionProductiva, on_delete=models.CASCADE)
#     def __str__(self):
#         return self.nombre
#-------------------------------
#
# class Continent(models.Model):
#     name = models.CharField(max_length=255)
#     def __str__(self):
#         return self.name
#
# class Country(models.Model):
#     continent = models.ForeignKey(Continent, on_delete=models.CASCADE)
#     name = models.CharField(max_length=255)
#     def __str__(self):
#         return self.name
#
#
#
# class Location(models.Model):
#     continent = models.ForeignKey(Continent, on_delete=models.CASCADE)
#     country = ChainedForeignKey(
#         Country,
#         chained_field="continent",
#         chained_model_field="continent",
#         show_all=False,
#         auto_choose=True,
#         sort=True, on_delete=models.CASCADE)
#
#     city = models.CharField(max_length=50)
#     street = models.CharField(max_length=100)