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
from django.urls import include, re_path
admin.site.site_header = 'Administración Instituciones Tecnológicas'
admin.site.index_title = 'Panel de control'
admin.site.site_title = 'Administración Instituciones Tecnológicas'
admin.site.site_url = ''

urlpatterns = [
    path('', view_home, name='home'),
    path('admin/', admin.site.urls),
    path('quienes_somos/', view_quienes_somos, name='quienes_somos'),
    path('instituciones_tecnologicas/', view_home, name='instituciones_tecnologicas'),
    path('instituciones_productivas/', view_home, name='instituciones_productivas'),
    path('mapa/', view_home, name='mapa'),
    path('contacto/', view_home, name='contacto'),
    re_path(r'^chaining/', include('smart_selects.urls')),
    path('', include('core.urls', namespace='core')),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)\
+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
