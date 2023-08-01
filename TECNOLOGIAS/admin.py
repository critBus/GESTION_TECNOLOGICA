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

class EspecieAdmin(admin.ModelAdmin):
    model = Especie
    formfield_overrides = STYLES_FORMFIELDS
admin.site.register(Especie,EspecieAdmin)

class TipoDeTecnologiaAdmin(admin.ModelAdmin):
    model = TipoDeTecnologia
    formfield_overrides = STYLES_FORMFIELDS
admin.site.register(TipoDeTecnologia,TipoDeTecnologiaAdmin)

from REPORTES.views import *
class TecnologiaAdmin(admin.ModelAdmin):
    model = Tecnologia
    formfield_overrides = STYLES_FORMFIELDS
    actions = [REPORTE_TECNOLOGIAS_PDF.getAction()]
admin.site.register(Tecnologia,TecnologiaAdmin)

