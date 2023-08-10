from django.contrib import admin

from .views import *
from django.forms import ClearableFileInput,TextInput
from django.contrib.admin.widgets import AdminFileWidget, FilteredSelectMultiple
from django.utils.safestring import mark_safe
from ckeditor.widgets import CKEditorWidget


from image_uploader_widget.widgets import ImageUploaderWidget
from solo.admin import SingletonModelAdmin
from nested_inline.admin import NestedStackedInline, NestedModelAdmin
from .models import *
from django.contrib.contenttypes.admin import GenericTabularInline
# Register your models here.

from django.contrib import admin
from django.utils.safestring import mark_safe
from django import forms
from REPORTES.views import *

from django.contrib.admin.widgets import AdminFileWidget

from CONFIGURACION.admin import *
from TECNOLOGIAS.admin import *
from django.contrib.admin.widgets import AdminFileWidget

from import_export import resources
from import_export.admin import ExportActionMixin, ImportExportActionModelAdmin
from import_export.widgets import ManyToManyWidget
from import_export.fields import Field
from GESTION_TECNOLOGICA.Utiles.UtilesParaExportar import *
class TipoDeInstitucionCientificaAdmin(admin.ModelAdmin):
    model = TipoDeInstitucionCientifica
    formfield_overrides = STYLES_FORMFIELDS
admin.site.register(TipoDeInstitucionCientifica,TipoDeInstitucionCientificaAdmin)




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



class InstitucionCientificaAdmin(ImportExportActionModelAdmin):#admin.ModelAdmin
    resource_class = InstitucionCientificaResource
    model = InstitucionCientifica
    formfield_overrides = STYLES_FORMFIELDS
    actions = [REPORTE_INSTITUCIONES_CIENTIFICA_PDF.getAction()]
    def get_form(self, request, obj=None, change=False, **kwargs):
        forms=super(InstitucionCientificaAdmin,self).get_form(request,obj,change,**kwargs)
        forms.base_fields['provincia'].widget.can_add_related = False
        forms.base_fields['provincia'].widget.can_change_related = False#can_view_related
        forms.base_fields['provincia'].widget.can_view_related = False

        forms.base_fields['municipio'].widget.can_add_related = False
        forms.base_fields['municipio'].widget.can_change_related = False  # can_view_related
        forms.base_fields['municipio'].widget.can_view_related = False
        return forms
admin.site.register(InstitucionCientifica,InstitucionCientificaAdmin)

