from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import path

from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, re_path
from .views import *

urlpatterns = [
    path('rellenar_instituciones_cientificas/',rellenar_instituciones_cientifica, name="rellenar_instituciones_cientificas"),
    path('rellenar_provincias/',rellenar_provincias, name="rellenar_provincias"),
    path('rellenar_provincias_municipios/',rellenar_provincias_municipios, name="rellenar_provincias_municipios"),
]