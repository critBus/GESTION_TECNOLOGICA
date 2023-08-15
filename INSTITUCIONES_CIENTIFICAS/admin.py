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
    list_display = ('nombre',)
    search_fields = (
    'nombre',)
    ordering = ('nombre',)
    date_hierarchy = 'created'
admin.site.register(TipoDeInstitucionCientifica,TipoDeInstitucionCientificaAdmin)




class InstitucionCientificaAdmin(ImportExportActionModelAdmin):#admin.ModelAdmin
    resource_class = InstitucionCientificaResource
    model = InstitucionCientifica
    formfield_overrides = STYLES_FORMFIELDS
    actions = [REPORTE_INSTITUCIONES_CIENTIFICA_PDF.getAction()]
    list_display = ('Nombre','NombreAbreviado','tipoDeInstitucionCientifica','provincia','municipio')
    search_fields = ('Nombre','NombreAbreviado','tipoDeInstitucionCientifica__nombre','provincia__nombre','municipio__nombre')
    list_filter = ('tipoDeInstitucionCientifica','provincia','municipio')
    ordering = ('Nombre','tipoDeInstitucionCientifica','provincia','municipio')
    date_hierarchy = 'created'
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






class EspecieAdmin(ImportExportActionModelAdmin):#admin.ModelAdmin
    resource_class = EspecieResource
    model = Especie
    formfield_overrides = STYLES_FORMFIELDS
    actions = [REPORTE_ESPECIES_PDF.getAction()]
    list_display = ('nombreCientifico', 'nombreComun', 'tipoDeEspecie')
    search_fields = (
        'nombreCientifico', 'nombreComun', 'tipoDeEspecie')
    list_filter = ('tipoDeEspecie',)
    ordering = ('nombreCientifico', 'nombreComun', 'tipoDeEspecie')
    date_hierarchy = 'created'
admin.site.register(Especie,EspecieAdmin)

class TipoDeTecnologiaAdmin(admin.ModelAdmin):
    model = TipoDeTecnologia
    formfield_overrides = STYLES_FORMFIELDS
    list_display = ('nombre',)
    search_fields = (
        'nombre',)
    ordering = ('nombre',)
    date_hierarchy = 'created'
admin.site.register(TipoDeTecnologia,TipoDeTecnologiaAdmin)




class TecnologiaAdmin(ImportExportActionModelAdmin):#admin.ModelAdmin
    resource_class = TecnologiaResource
    model = Tecnologia
    formfield_overrides = STYLES_FORMFIELDS
    actions = [REPORTE_TECNOLOGIAS_PDF.getAction()]
    list_display = ('nombre', 'accionEsperada', 'tipoDeTecnologia')
    search_fields = (
    'nombre', 'accionEsperada', 'tipoDeTecnologia__nombre')
    list_filter = ('accionEsperada', 'tipoDeTecnologia')
    ordering = ('nombre', 'accionEsperada', 'tipoDeTecnologia')
    date_hierarchy = 'created'
admin.site.register(Tecnologia,TecnologiaAdmin)

