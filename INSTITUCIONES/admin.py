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

# Register your models here.

STYLES_FORMFIELDS={models.ImageField: {'widget': ImageUploaderWidget},
                           models.TextField: {'widget': CKEditorWidget},
                           models.CharField: {'widget': TextInput(attrs={"size": "100"})}
                           }

class Informacion_PrincipalInline(NestedStackedInline):
    model = Informacion_Principal
    extra = 1
    fk_name = 'Pagina'
    formfield_overrides = STYLES_FORMFIELDS

class ImagenesFondo_PrincipalInline(NestedStackedInline):
    model = ImagenesFondo_Principal
    extra = 1
    fk_name = 'Pagina'
    formfield_overrides = STYLES_FORMFIELDS

class PaginaPrincipalAdmin(SingletonModelAdmin):
    model = PaginaPrincipal
    inlines = [ImagenesFondo_PrincipalInline,Informacion_PrincipalInline]
    formfield_overrides = STYLES_FORMFIELDS

admin.site.register(PaginaPrincipal, PaginaPrincipalAdmin)

class ConfiguracionGeneralAdmin(SingletonModelAdmin):
    model = ConfiguracionGeneral
    formfield_overrides = STYLES_FORMFIELDS
admin.site.register(ConfiguracionGeneral, ConfiguracionGeneralAdmin)

