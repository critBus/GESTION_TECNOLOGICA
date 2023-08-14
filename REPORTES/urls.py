from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import path

from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, re_path
from .views import *
#
urlpatterns = [
    path('institucion_productiva/reporte/pdf/',REPORTE_INSTITUCIONES_PRODUCTIVA_PDF.getView())
    ,path('institucion_productiva/reporte/csv/',REPORTE_INSTITUCIONES_PRODUCTIVA_PDF.getEndPoint_CSV())
    ,path('institucion_productiva/reporte/exel/',REPORTE_INSTITUCIONES_PRODUCTIVA_PDF.getEndPoint_Exel())

    ,path('institucion_cientifica/reporte/pdf/',REPORTE_INSTITUCIONES_CIENTIFICA_PDF.getView())
    ,path('institucion_cientifica/reporte/csv/',REPORTE_INSTITUCIONES_CIENTIFICA_PDF.getEndPoint_CSV())
    ,path('institucion_cientifica/reporte/exel/',REPORTE_INSTITUCIONES_CIENTIFICA_PDF.getEndPoint_Exel())

    ,path('tecnologia/reporte/pdf/',REPORTE_TECNOLOGIAS_PDF.getView())
    ,path('tecnologia/reporte/csv/',REPORTE_TECNOLOGIAS_PDF.getEndPoint_CSV())
    ,path('tecnologia/reporte/exel/',REPORTE_TECNOLOGIAS_PDF.getEndPoint_Exel())

    ,path('especie/reporte/pdf/',REPORTE_ESPECIES_PDF.getView())
    ,path('especie/reporte/csv/',REPORTE_ESPECIES_PDF.getEndPoint_CSV())
    ,path('especie/reporte/exel/',REPORTE_ESPECIES_PDF.getEndPoint_Exel())

    ,path('productos/reporte/pdf/',REPORTE_PRODUCTOS_PDF.getView())
    ,path('productos/reporte/csv/',REPORTE_PRODUCTOS_PDF.getEndPoint_CSV())
    ,path('productos/reporte/exel/',REPORTE_PRODUCTOS_PDF.getEndPoint_Exel())
    # path('personas_pdf/',login_required(INSTITUCIONES_PRODUCTIVA_PDF), name="personas_pdf"),
]