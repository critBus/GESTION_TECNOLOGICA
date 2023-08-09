from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from .models import *
import os
from django.views import generic
from GESTION_TECNOLOGICA.Utiles.LocalizacionDePagina import *
from CONFIGURACION.models import *
from INSTITUCIONES_CIENTIFICAS.models import *
import random


class Tecnologia_ListView(generic.ListView):
    model = Tecnologia
    paginate_by=10
    def get_queryset(self):
        queryset = super().get_queryset()
        q = self.request.GET.get('q')
        campo = self.request.GET.get('campo')
        if q and campo:
            q = q.strip()
            if campo=='accionEsperada':
                queryset = queryset.filter(accionEsperada__icontains=q)
            elif campo=='Tipo':
                queryset = queryset.filter(tipoDeTecnologia__nombre__icontains=q)

            elif campo=='especie_nombreComun':
                queryset = queryset.filter(especies__nombreComun__icontains=q)
            elif campo=='especie_nombreCientifico':
                queryset = queryset.filter(especies__nombreCientifico__icontains=q)
            elif campo=='especie_tipoDeEspecie':
                queryset = queryset.filter(especies__tipoDeEspecie__icontains=q)


            else:
                queryset = queryset.filter(nombre__icontains=q)
        return queryset
    def get_context_data(self, *a, object_list=None, **kwargs):
        context=super().get_context_data(*a,object_list=object_list,**kwargs)
        config = ConfiguracionGeneral.get_solo()
        lcp = LocalizacionDePagina("Servicios","Lista", "Tipos De Tecnologías")
        context['config']=config
        context['lcp'] = lcp
        context['urlPdf'] = '/reporte_tecnologia_pdf/'
        return context


class Tecnologia_DetailView(generic.DetailView):
    model = Tecnologia
    def get_context_data(self, *a, object_list=None, **kwargs):
        context=super().get_context_data(*a,object_list=object_list,**kwargs)
        config = ConfiguracionGeneral.get_solo()
        lcp = LocalizacionDePagina("Servicios","Detalles", "Tipo De Tecnología")
        context['config']=config
        context['lcp'] = lcp
        context['industrias'] = InstitucionCientifica.objects.filter(tecnologias=context['object'])

        return context




class Especie_ListView(generic.ListView):
    model = Especie
    paginate_by=10
    def get_queryset(self):
        queryset = super().get_queryset()
        q = self.request.GET.get('q')
        campo = self.request.GET.get('campo')
        if q and campo:
            q = q.strip()
            if campo=='nombreComun':
                queryset = queryset.filter(nombreComun__icontains=q)
            elif campo=='nombreCientifico':
                queryset = queryset.filter(nombreCientifico__icontains=q)
            elif campo=='tipoDeEspecie':
                queryset = queryset.filter(tipoDeEspecie__icontains=q)


            else:
                queryset = queryset.filter(nombreComun__icontains=q)
        return queryset
    def get_context_data(self, *a, object_list=None, **kwargs):
        context=super().get_context_data(*a,object_list=object_list,**kwargs)
        config = ConfiguracionGeneral.get_solo()
        lcp = LocalizacionDePagina("Servicios","Lista", "Tipos De Especies")
        context['config']=config
        context['lcp'] = lcp
        context['urlPdf'] = '/reporte_especie_pdf/'
        return context

#
# class Especie_DetailView(generic.DetailView):
#     model = Tecnologia
#     def get_context_data(self, *a, object_list=None, **kwargs):
#         context=super().get_context_data(*a,object_list=object_list,**kwargs)
#         config = ConfiguracionGeneral.get_solo()
#         lcp = LocalizacionDePagina("Servicios","Detalles", "Tipo De Tecnología")
#         context['config']=config
#         context['lcp'] = lcp
#         context['industrias'] = InstitucionCientifica.objects.filter(tecnologias=context['object'])
#
#         return context