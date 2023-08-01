from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import path

from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, re_path
from .views import *
#
urlpatterns = [
    # path('reporte_personas_pdf/',login_required(reporte_INSTITUCIONES_PRODUCTIVA_PDF), name="reporte_personas_pdf"),
]