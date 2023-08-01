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
from TECNOLOGIAS.admin import *

class TipoDeInstitucionCientificaAdmin(admin.ModelAdmin):
    model = TipoDeInstitucionCientifica
    formfield_overrides = STYLES_FORMFIELDS
admin.site.register(TipoDeInstitucionCientifica,TipoDeInstitucionCientificaAdmin)

from REPORTES.views import *
class InstitucionCientificaAdmin(admin.ModelAdmin):
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

