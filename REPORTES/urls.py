from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import path

from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, re_path
from .views import *
#
urlpatterns = [
    path('reporte_institucion_productiva_pdf/',REPORTE_INSTITUCIONES_PRODUCTIVA_PDF.getView())
    ,path('reporte_institucion_cientifica_pdf/',REPORTE_INSTITUCIONES_CIENTIFICA_PDF.getView())
    ,path('reporte_tecnologia_pdf/',REPORTE_TECNOLOGIAS_PDF.getView())
    ,path('reporte_especie_pdf/',REPORTE_ESPECIES_PDF.getView())
    ,path('reporte_productos_pdf/',REPORTE_PRODUCTOS_PDF.getView())
    # path('reporte_personas_pdf/',login_required(reporte_INSTITUCIONES_PRODUCTIVA_PDF), name="reporte_personas_pdf"),
]