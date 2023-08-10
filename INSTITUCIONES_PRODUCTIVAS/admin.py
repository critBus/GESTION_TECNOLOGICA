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
from import_export.fields import Field

from CONFIGURACION.admin import *
from TECNOLOGIAS.admin import *


class TipoDeInstitucionProductivaAdmin(admin.ModelAdmin):
    model = TipoDeInstitucionProductiva
    formfield_overrides = STYLES_FORMFIELDS
admin.site.register(TipoDeInstitucionProductiva,TipoDeInstitucionProductivaAdmin)

class TipoDeProductoAdmin(admin.ModelAdmin):
    model = TipoDeProducto
    formfield_overrides = STYLES_FORMFIELDS
admin.site.register(TipoDeProducto,TipoDeProductoAdmin)


class ProductoInline(NestedStackedInline):#admin.TabularInline
    model = Producto
    extra = 1
    fk_name = 'institucionProductiva'
    formfield_overrides = STYLES_FORMFIELDS
    # form =

    # def get_form(self, request, obj=None, change=False, **kwargs):
    #     forms = super(ProductoInline, self).get_form(request, obj, change, **kwargs)
    #     forms.base_fields['tipoDeProducto'].widget.can_add_related = False
    #     forms.base_fields['tipoDeProducto'].widget.can_change_related = False  # can_view_related
    #     forms.base_fields['tipoDeProducto'].widget.can_view_related = False
    #
    #
    #
    #     return forms


class InstitucionProductivaResource(resources.ModelResource):
    class Meta:
        model = InstitucionProductiva
        fields = ('Nombre', 'NombreAbreviado')
        export_order = ('Nombre', 'NombreAbreviado')


from REPORTES.views import *
class InstitucionProductivaAdmin(ImportExportActionModelAdmin):#admin.ModelAdmin
    resource_class = InstitucionProductivaResource
    model = InstitucionProductiva
    formfield_overrides = STYLES_FORMFIELDS
    inlines = [ProductoInline]
    actions = [REPORTE_INSTITUCIONES_PRODUCTIVA_PDF.getAction()]
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

