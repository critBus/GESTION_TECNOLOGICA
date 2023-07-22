from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.conf import settings
from django import forms
from django.utils.html import format_html
# Create your models here.

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


class ConfiguracionGeneral(SingletonModel):
    nombreSitio=models.CharField(max_length=20,verbose_name="Sitio",null=True)
    ImagenLogo = models.ImageField(upload_to='config')
    linkFacebook=models.CharField(max_length=255,verbose_name="Link Facebook",null=True)
    linkTwitter = models.CharField(max_length=255, verbose_name="Link Twitter",null=True)
    linkYoutube= models.CharField(max_length=255, verbose_name="Link Youtube",null=True)
    correo=models.EmailField(null=True)
    telefono=models.CharField(max_length=8,null=True)#, widget=CustomTelefotoWidget
    direccion=models.CharField(max_length=255,verbose_name="Dirección",null=True)
    horarios = models.TextField()
    ImagenBreadcrumbs = models.ImageField(upload_to='config')



    def __str__(self):
        return "Configuración General"

    class Meta:
        verbose_name = "Configuración General"

class PaginaPrincipal(SingletonModel):
    Titulo = models.CharField(max_length=255 )
    Descripcion = models.TextField()
    #Imagen = models.ImageField(upload_to='paginaPrincipal')

    def __str__(self):
        return "Pagina Principal"

    class Meta:
        verbose_name = "Pagina Principal"



class ImagenesFondo_Principal(models.Model):
    class Meta:
        verbose_name = 'Imágen Fondo'
        verbose_name_plural = 'Imágenes Fondo'

    Imagen = models.ImageField(upload_to='ImagenesFondo_Principal')
    Pagina = models.ForeignKey(PaginaPrincipal, on_delete=models.CASCADE, related_name="pagina_principal_imagenesFondo")

    def __str__(self):
        return "Imágen Fondo"

class Informacion_Principal(models.Model):
    class Meta:
        verbose_name = 'Información Principal '
        verbose_name_plural = 'Informaciones Principales'
    Pagina = models.ForeignKey(PaginaPrincipal, on_delete=models.CASCADE,related_name="pagina_principal_informacion")
    Titulo = models.CharField(max_length=255)
    Descripcion = models.TextField()
    Imagen = models.ImageField(upload_to='Informacion_Principal')

    def __str__(self):
        return  self.Titulo
