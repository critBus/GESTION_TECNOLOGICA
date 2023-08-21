from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from .models import *
import os
from django.views import generic
from GESTION_TECNOLOGICA.Utiles.LocalizacionDePagina import *
import random
def rellenar_instituciones_cientifica(request):
    class LT:
        def __init__(self):
            self.lt = TipoDeInstitucionCientifica.objects.all()
            self.indice = 0
            self.size=len(self.lt)
        def get(self):
            r=self.lt[self.indice]
            self.indice=(self.indice+1)%self.size
            return r
    lt=LT()
    class LIm:
        def __init__(self):
            self.lt = ["1.jpg","cvive.png","Edel.jpg"]
            self.indice = 0
            self.size=len(self.lt)
            self.carpeta="InstitucionCientifica"
        def get(self):
            r=os.path.join(self.carpeta, self.lt[self.indice])
            self.indice=(self.indice+1)%self.size
            return r
    lim=LIm()
    class RTtc:
        def __init__(self):
            self.list_tec=Tecnologia.objects.all()
            self.cantidad=len(self.list_tec)
        def addRandomTec(self,p:InstitucionCientifica):
            for t in self.list_tec:
                if random.randrange(2)==1:
                    p.tecnologias.add(t)
    rtc=RTtc()
    for i in range(50):

        p=InstitucionCientifica()
        p.Direccion="dire "+str(i)
        p.NombreAbreviado="Abre "+str(i)

        p.tipoDeInstitucionCientifica=lt.get()
        p.Nombre="nombre"+str(i)
        p.Imagen=lim.get()
        p.Contacto="Contacto"+str(i)
        p.municipio=Municipio.objects.filter(nombre="Jaruco").first()
        p.provincia=Provincia.objects.filter(nombre="Mayabeque").first()
        p.Correo="asd"+str(i)+"@gmail.com"
        p.Telefono="123123123"+str(i)
        p.save()

        rtc.addRandomTec(p)
        p.save()

    return JsonResponse({'status': 'ok'}, status=200)




class InstitucionCientifica_ListView(generic.ListView):
    model = InstitucionCientifica
    paginate_by=10
    def get_queryset(self):
        queryset = super().get_queryset()
        q = self.request.GET.get('q')
        campo = self.request.GET.get('campo')
        if q and campo:
            q = q.strip()
            if campo=='NombreAbreviado':
                queryset = queryset.filter(NombreAbreviado__icontains=q)
            elif campo=='Contacto':
                queryset = queryset.filter(Contacto__icontains=q)
            elif campo=='Telefono':
                queryset = queryset.filter(Telefono__icontains=q)
            elif campo=='Correo':
                queryset = queryset.filter(Correo__icontains=q)
            elif campo=='Provincia':
                queryset = queryset.filter(provincia__nombre__icontains=q)
            elif campo=='Municipio':
                queryset = queryset.filter(municipio__nombre__icontains=q)
            elif campo=='Tipo':
                queryset = queryset.filter(tipoDeInstitucionCientifica__nombre__icontains=q)
            elif campo=='Tecnologia':
                queryset = queryset.filter(tecnologias__nombre__icontains=q)
            elif campo=='TipoDeTecnologia':
                queryset = queryset.filter(tecnologias__tipoDeTecnologia__nombre__icontains=q)
            else:
                queryset = queryset.filter(Nombre__icontains=q)
        return queryset
    def get_context_data(self, *a, object_list=None, **kwargs):
        context=super().get_context_data(*a,object_list=object_list,**kwargs)
        config = ConfiguracionGeneral.get_solo()
        lcp = LocalizacionDePagina("Instituciones","Lista", "Instituciones Científicas")
        context['config']=config
        context['lcp'] = lcp
        context['urlExportar'] = '/institucion_cientifica'

        context['tipos'] = TipoDeInstitucionCientifica.objects.all()
        context['tiposTecnologia'] = TipoDeTecnologia.objects.all()

        context['provincias'] = Provincia.objects.all()
        context['municipios'] = Municipio.objects.all()#.distinct("nombre")

        lista=self.get_queryset()#self.queryset#context['object_list']

        context['listaPuntos'] =[{
            "latitud":v.latitud
            ,"longitud":v.longitud
            ,"textoAMostrar":v.NombreAbreviado
        } for v in lista]
        return context


class InstitucionCientifica_DetailView(generic.DetailView):
    model = InstitucionCientifica
    def get_context_data(self, *a, object_list=None, **kwargs):
        context=super().get_context_data(*a,object_list=object_list,**kwargs)
        config = ConfiguracionGeneral.get_solo()
        lcp = LocalizacionDePagina("Instituciones","Detalles", "Institucion Científica")
        context['config']=config
        context['lcp'] = lcp

        return context






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
        context['urlExportar'] = '/tecnologia'

        context['tipos'] = TipoDeTecnologia.objects.all()

        lista = self.get_queryset()  # self.queryset#context['object_list']

        listaI =InstitucionCientifica.objects.filter(
            tecnologias__in=lista)


        context['listaPuntos'] = [{
            "latitud": v.latitud
            , "longitud": v.longitud
            , "textoAMostrar": v.NombreAbreviado+" | "+" | ".join([j.nombre for j in v.tecnologias.all()]) #+" | "+
        } for v in listaI]

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
        context['urlExportar'] = '/especie'

        lista = self.get_queryset()  # self.queryset#context['object_list']

        listaT = Tecnologia.objects.filter(
            especies__in=lista)

        listaI = InstitucionCientifica.objects.filter(
            tecnologias__in=listaT)
        def getListaNombre(institucion:InstitucionCientifica):

            ln=[]
            for t in institucion.tecnologias.all():
                for e in t.especies.all():
                    if not e.nombreCientifico in ln:
                        ln.append(e.nombreCientifico)
            return ln
        context['listaPuntos'] = [{
            "latitud": v.latitud
            , "longitud": v.longitud
            , "textoAMostrar": v.NombreAbreviado + " | " + " | ".join(getListaNombre(v))
            # +" | "+
        } for v in listaI]

        return context

#
class Especie_DetailView(generic.DetailView):
    model = Especie
    def get_context_data(self, *a, object_list=None, **kwargs):
        context=super().get_context_data(*a,object_list=object_list,**kwargs)
        config = ConfiguracionGeneral.get_solo()
        lcp = LocalizacionDePagina("Servicios","Detalles", "Tipo De Especie")
        context['config']=config
        context['lcp'] = lcp
        context['industrias'] = InstitucionCientifica.objects.filter(
            tecnologias__in=Tecnologia.objects.filter(especies=context['object']))

        return context