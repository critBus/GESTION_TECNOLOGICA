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

from django.contrib.admin.widgets import AdminFileWidget

from CONFIGURACION.admin import *
from import_export import resources
from import_export.admin import ExportActionMixin, ImportExportActionModelAdmin
from import_export.widgets import ManyToManyWidget
from import_export.fields import Field
from GESTION_TECNOLOGICA.Utiles.UtilesParaExportar import *
from REPORTES.views import *



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

