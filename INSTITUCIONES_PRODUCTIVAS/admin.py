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

from import_export import resources
from import_export.admin import ExportActionMixin, ImportExportActionModelAdmin
from import_export.widgets import ManyToManyWidget
from import_export.fields import Field

from CONFIGURACION.admin import *
from TECNOLOGIAS.admin import *
from GESTION_TECNOLOGICA.Utiles.UtilesParaExportar import *

class TipoDeInstitucionProductivaAdmin(admin.ModelAdmin):
    model = TipoDeInstitucionProductiva
    formfield_overrides = STYLES_FORMFIELDS
    list_display = ('nombre',)
    search_fields = (
        'nombre',)
    ordering = ('nombre',)
    date_hierarchy = 'created'
admin.site.register(TipoDeInstitucionProductiva,TipoDeInstitucionProductivaAdmin)

class TipoDeProductoAdmin(admin.ModelAdmin):
    model = TipoDeProducto
    formfield_overrides = STYLES_FORMFIELDS
    list_display = ('nombre',)
    search_fields = (
        'nombre',)
    ordering = ('nombre',)
    date_hierarchy = 'created'
admin.site.register(TipoDeProducto,TipoDeProductoAdmin)


class ProductoAdmin(admin.ModelAdmin):#admin.TabularInline
    model = Producto
    extra = 1
    fk_name = 'institucionProductiva'
    formfield_overrides = STYLES_FORMFIELDS

admin.site.register(Producto,ProductoAdmin)


from REPORTES.views import *


class InstitucionProductivaForm(forms.ModelForm):
    class Meta:
        model=InstitucionProductiva
        fields='__all__'
    def __init__(self,*args,**kwargs):
        super(InstitucionProductivaForm, self).__init__(*args,**kwargs)
        self.fields['productos'].label_from_instance=lambda obj:str(obj)+(" | "+str(obj.tipoDeProducto) if obj.tipoDeProducto else "")
        self.fields['productos'].queryset=Producto.objects.order_by("nombre")


class InstitucionProductivaAdmin(ImportExportActionModelAdmin):#admin.ModelAdmin
    resource_class = InstitucionProductivaResource
    model = InstitucionProductiva
    formfield_overrides = STYLES_FORMFIELDS
    #inlines = [ProductoInline]
    actions = [REPORTE_INSTITUCIONES_PRODUCTIVA_PDF.getAction()]
    list_display = ('Nombre', 'NombreAbreviado', 'tipoDeInstitucionProductiva', 'provincia', 'municipio')
    search_fields = ('Nombre', 'NombreAbreviado', 'tipoDeInstitucionProductiva__nombre', 'provincia__nombre', 'municipio__nombre')
    list_filter = ('tipoDeInstitucionProductiva', 'provincia', 'municipio')#,'producto_set__tipoDeProducto__nombre'
    ordering = ('Nombre', 'tipoDeInstitucionProductiva', 'provincia', 'municipio')
    date_hierarchy = 'created'
    filter_horizontal = ('productos',)
    form = InstitucionProductivaForm


    def get_form(self, request, obj=None, change=False, **kwargs):
        forms=super(InstitucionProductivaAdmin,self).get_form(request,obj,change,**kwargs)
        forms.base_fields['provincia'].widget.can_add_related = False
        forms.base_fields['provincia'].widget.can_change_related = False#can_view_related
        forms.base_fields['provincia'].widget.can_view_related = False

        forms.base_fields['municipio'].widget.can_add_related = False
        forms.base_fields['municipio'].widget.can_change_related = False  # can_view_related
        forms.base_fields['municipio'].widget.can_view_related = False

        # print(vars(forms))


        return forms
admin.site.register(InstitucionProductiva,InstitucionProductivaAdmin)


# class ProductoResource(resources.ModelResource):
#     class Meta:
#         model = Producto
#         fields = ('nombre', 'tipoDeProducto')
#         export_order = ('nombre', 'tipoDeProducto')
# class ProductoAdmin(ImportExportActionModelAdmin):
#     resource_class = ProductoResource
#     model = Producto
#     formfield_overrides = STYLES_FORMFIELDS
#
# admin.site.register(Producto,ProductoAdmin)

