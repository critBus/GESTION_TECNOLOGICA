"""GESTION_TECNOLOGICA URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from django.conf import settings
from django.conf.urls.static import static

from INSTITUCIONES.views import *
from INSTITUCIONES_PRODUCTIVAS.views import *
from INSTITUCIONES_CIENTIFICAS.views import *
from TECNOLOGIAS.views import *
from django.urls import include, re_path
admin.site.site_header = 'Administración Instituciones Tecnológicas'
admin.site.index_title = 'Panel de control'
admin.site.site_title = 'Administración Instituciones Tecnológicas'
admin.site.site_url = ''

urlpatterns = [
    path('', view_home, name='home'),
    path('admin/', admin.site.urls),
    path('quienes_somos/', view_quienes_somos, name='quienes_somos'),
    path('instituciones_tecnologicas/', InstitucionCientifica_ListView.as_view(), name='instituciones_tecnologicas'),
    path('instituciones_tecnologicas/findById/<int:pk>', InstitucionCientifica_DetailView.as_view()),
    path('instituciones_productivas/', InstitucionProductiva_ListView.as_view(), name='instituciones_productivas'),
    path('instituciones_productivas/findById/<int:pk>', InstitucionProductiva_DetailView.as_view()),
    path('Servicios/Tecnologias/lista', Tecnologia_ListView.as_view(), name='tecnologias'),
    path('Servicios/Tecnologias/findById/<int:pk>', Tecnologia_DetailView.as_view()),
    path('Servicios/Productos/lista', Producto_ListView.as_view(), name='productos'),
    path('Servicios/Productos/findById/<int:pk>', Producto_DetailView.as_view()),
    path('Servicios/Especies/lista', Especie_ListView.as_view(), name='especies'),
    path('Servicios/Especies/findById/<int:pk>', Especie_DetailView.as_view()),
    path('mapa/', view_home, name='mapa'),
    path('contacto/', view_home, name='contacto'),
    re_path(r'^chaining/', include('smart_selects.urls')),
    path('', include('REPORTES.urls')),#, namespace='REPORTES'
    path('', include('INSTITUCIONES_PRODUCTIVAS.urls')),
    path('', include('INSTITUCIONES_CIENTIFICAS.urls')),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)\
+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
