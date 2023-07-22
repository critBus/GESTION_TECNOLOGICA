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

class AdminImageWidget(AdminFileWidget):
    def render(self, name, value, attrs=None, renderer=None):
        output = []
        if value and getattr(value, "url", None):
            image_url = value.url
            file_name = str(value)
            output.append(u' <a href="%s" target="_blank"><img src="%s" alt="%s" width="150" height="150"  style="object-fit: cover;"/></a> %s ' % \
                (image_url, image_url, file_name, ""))
        output.append(super(AdminFileWidget, self).render(name, value, attrs))
        return mark_safe(u''.join(output))


STYLES_FORMFIELDS={models.ImageField: {'widget': AdminImageWidget},#ImageUploaderWidget
                           models.TextField: {'widget': CKEditorWidget},
                           models.CharField: {'widget': TextInput(attrs={"size": "100"})}
                           }

class Informacion_PrincipalInline(NestedStackedInline):#admin.TabularInline
    model = Informacion_Principal
    extra = 1
    #fk_name = 'Pagina'
    formfield_overrides = STYLES_FORMFIELDS

class ImagenesFondo_PrincipalInline(NestedStackedInline):#NestedStackedInline
    model = ImagenesFondo_Principal
    extra = 1
    #fk_name = 'Pagina'
    formfield_overrides = STYLES_FORMFIELDS

    # readonly_fields = ('image_preview',)
    #
    # def image_preview(self, obj):
    #     # ex. the name of column is "image"
    #     if obj.Imagen:
    #         return mark_safe(
    #             '<img src="{0}" width="150" height="150" style="object-fit:contain" />'.format(obj.Imagen.url))
    #     else:
    #         return '(No image)'
    #
    # image_preview.short_description = 'Preview'

class PaginaPrincipalAdmin(SingletonModelAdmin):
    model = PaginaPrincipal
    inlines = [ImagenesFondo_PrincipalInline,Informacion_PrincipalInline]
    formfield_overrides = STYLES_FORMFIELDS

admin.site.register(PaginaPrincipal, PaginaPrincipalAdmin)

class ConfiguracionGeneralAdmin(SingletonModelAdmin):
    model = ConfiguracionGeneral
    formfield_overrides = STYLES_FORMFIELDS
admin.site.register(ConfiguracionGeneral, ConfiguracionGeneralAdmin)



class EspecieAdmin(admin.ModelAdmin):
    model = Especie
    formfield_overrides = STYLES_FORMFIELDS
admin.site.register(Especie,EspecieAdmin)

class TipoDeTecnologiaAdmin(admin.ModelAdmin):
    model = TipoDeTecnologia
    formfield_overrides = STYLES_FORMFIELDS
admin.site.register(TipoDeTecnologia,TipoDeTecnologiaAdmin)


class TecnologiaAdmin(admin.ModelAdmin):
    model = Tecnologia
    formfield_overrides = STYLES_FORMFIELDS
admin.site.register(Tecnologia,TecnologiaAdmin)


class TipoDeInstitucionCientificaAdmin(admin.ModelAdmin):
    model = TipoDeInstitucionCientifica
    formfield_overrides = STYLES_FORMFIELDS
admin.site.register(TipoDeInstitucionCientifica,TipoDeInstitucionCientificaAdmin)

class InstitucionCientificaAdmin(admin.ModelAdmin):
    model = InstitucionCientifica
    formfield_overrides = STYLES_FORMFIELDS
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

class InstitucionProductivaAdmin(admin.ModelAdmin):
    model = InstitucionProductiva
    formfield_overrides = STYLES_FORMFIELDS
    inlines = [ProductoInline]
    def get_form(self, request, obj=None, change=False, **kwargs):
        forms=super(InstitucionProductivaAdmin,self).get_form(request,obj,change,**kwargs)
        forms.base_fields['provincia'].widget.can_add_related = False
        forms.base_fields['provincia'].widget.can_change_related = False#can_view_related
        forms.base_fields['provincia'].widget.can_view_related = False

        forms.base_fields['municipio'].widget.can_add_related = False
        forms.base_fields['municipio'].widget.can_change_related = False  # can_view_related
        forms.base_fields['municipio'].widget.can_view_related = False
        return forms
admin.site.register(InstitucionProductiva,InstitucionProductivaAdmin)

#-------------------------------
admin.site.register(Provincia)
admin.site.register(Municipio)
# admin.site.register(Continent)
# admin.site.register(Country)
#
#
#
# class LocationAdmin(admin.ModelAdmin):
#     #forms=LocationForm
#     def get_form(self, request, obj=None, change=False, **kwargs):
#         forms=super(LocationAdmin,self).get_form(request,obj,change,**kwargs)
#         #print(vars(forms.base_fields['continent'].widget))
#         forms.base_fields['continent'].widget.can_add_related = False
#         forms.base_fields['continent'].widget.can_change_related = False#can_view_related
#         forms.base_fields['continent'].widget.can_view_related = False
#
#         forms.base_fields['country'].widget.can_add_related = False
#         forms.base_fields['country'].widget.can_change_related = False  # can_view_related
#         forms.base_fields['country'].widget.can_view_related = False
#         return forms
# admin.site.register(Location,LocationAdmin)

