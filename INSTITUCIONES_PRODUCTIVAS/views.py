from django.http import JsonResponse
from django.shortcuts import render
from .models import *
# Create your views here.
import os
from django.views import generic
from GESTION_TECNOLOGICA.Utiles.LocalizacionDePagina import *
from django.db.models import Q
from GESTION_TECNOLOGICA.Utiles.UtilesGenerales import *
def rellenar_instituciones_productivas(request):
    class LT:
        def __init__(self):
            self.lt = TipoDeInstitucionProductiva.objects.all()
            self.indiceInstitucionProductiva = 0
            self.size=len(self.lt)
        def get(self):
            r=self.lt[self.indiceInstitucionProductiva]
            self.indiceInstitucionProductiva=(self.indiceInstitucionProductiva+1)%self.size
            return r
    lt=LT()
    class LIm:
        def __init__(self):
            self.lt = ["1.jpg","cvive.png","Edel.jpg"]
            self.indice = 0
            self.size=len(self.lt)
            self.carpeta="InstitucionProductiva"
        def get(self):
            r=os.path.join(self.carpeta, self.lt[self.indice])
            self.indice=(self.indice+1)%self.size
            return r
    lim=LIm()
    for i in range(50):
        p=InstitucionProductiva()
        p.Direccion="dire "+str(i)
        p.NombreAbreviado="Abre "+str(i)
        p.capacidadDeRefrigeracion=10+i
        p.tipoDeInstitucionProductiva=lt.get()
        p.Nombre="nombre"+str(i)
        p.Imagen=lim.get()
        p.Contacto="Contacto"+str(i)
        p.municipio=Municipio.objects.filter(nombre="Jaruco").first()
        p.provincia=Provincia.objects.filter(nombre="Mayabeque").first()
        p.Correo="asd"+str(i)+"@gmail.com"
        p.Telefono="123123123"+str(i)
        p.save()

    return JsonResponse({'status': 'ok'}, status=200)

class InstitucionProductiva_ListView(generic.ListView):
    model = InstitucionProductiva
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
            elif campo=='ProvinciaYMunicipio':
                provincia,municipio=getProvinciMunicipioDeQ(q)
                if municipio == "Todos":
                    queryset= queryset.filter(provincia__nombre__icontains=provincia)
                else:
                    queryset = queryset.filter(provincia__nombre__icontains=provincia
                                           ,municipio__nombre__icontains=municipio)
            elif campo=='Tipo':
                queryset = queryset.filter(tipoDeInstitucionProductiva__nombre__icontains=q)
            elif campo=='Producto':
                queryset = Producto.objects.filter(nombre__icontains=q)
                # cantidad=queryset.count()
                # print(cantidad)
                queryset = InstitucionProductiva.objects.filter(productos__in=queryset)
                # cantidad = queryset.count()
                # print(cantidad)
            elif campo=='TipoDeProducto':
                queryset = Producto.objects.filter(tipoDeProducto__nombre__icontains=q)
                queryset = InstitucionProductiva.objects.filter(productos__in=queryset)
            elif campo=='TieneAlamacenConRefrigeracion':
                queryset = queryset.filter(TieneAlamacenConRefrigeracion__icontains=q)
            else:
                queryset = queryset.filter(Nombre__icontains=q)
        return queryset
    def get_context_data(self, *a, object_list=None, **kwargs):
        context=super().get_context_data(*a,object_list=object_list,**kwargs)
        config = ConfiguracionGeneral.get_solo()
        lcp = LocalizacionDePagina("Instituciones","Lista", "Instituciones Productivas")
        context['config']=config
        context['lcp'] = lcp
        context['urlExportar'] = '/institucion_productiva'

        context['tipos'] = TipoDeInstitucionProductiva.objects.all()
        context['tiposProductos'] = TipoDeProducto.objects.all()

        context['provincias'] = Provincia.objects.all()
        context['municipios'] = Municipio.objects.all()#.distinct("nombre")
        lpm=[]
        lp=Provincia.objects.all()
        for p in lp:
            lm=Municipio.objects.filter(provincia=p)
            lsm=['Todos']
            for m in lm:
                lsm.append(m)
            lpm.append([p.nombre,lsm])#[ v.nombre for v in lm]

        context['ProvinciaYMunicipio']=lpm

        lista = self.get_queryset()  # self.queryset#context['object_list']

        context['listaPuntos'] = [{
            "latitud": v.latitud
            , "longitud": v.longitud
            , "textoAMostrar": v.NombreAbreviado
            , "url": "/instituciones_productivas/findById/" + str(v.id)
        } for v in lista]

        return context


class InstitucionProductiva_DetailView(generic.DetailView):
    model = InstitucionProductiva
    def get_context_data(self, *a, object_list=None, **kwargs):
        context=super().get_context_data(*a,object_list=object_list,**kwargs)
        config = ConfiguracionGeneral.get_solo()
        lcp = LocalizacionDePagina("Instituciones","Detalles", "Institucion Productiva")
        context['config']=config
        context['lcp'] = lcp

        dato=context['object']
        context['listaPuntos'] = [{
            "latitud": v.latitud
            , "longitud": v.longitud
            , "textoAMostrar": v.NombreAbreviado
            , "url": "/instituciones_productivas/findById/" + str(v.id)
        } for v in [dato]]

        context['nombreProvincia']=dato.provincia.nombre

        return context

class InstitucionYProductos:
    def __init__(self,institucion):
        self.institucion=institucion
        self.productos=[]
        self.ln=[]
    def add(self,p:Producto):
        if not p.nombre in self.ln:
            self.ln.append(p.nombre)
            self.productos.append(p)

class InstitucionesYProductos:
    def __init__(self):
        self.institucionesYProductos:Dict[InstitucionYProductos]={}


    def add(self,p:Producto):
        ni=p.institucionProductiva.Nombre
        if not ni in self.institucionesYProductos:
            self.institucionesYProductos[ni]=InstitucionYProductos(p.institucionProductiva)
        self.institucionesYProductos[ni].add(p)

class Producto_ListView(generic.ListView):
    model = Producto
    paginate_by=10
    def get_queryset(self):
        queryset = super().get_queryset()
        q = self.request.GET.get('q')
        campo = self.request.GET.get('campo')
        if q and campo:
            q = q.strip()
            if campo=='nombre':
                queryset = queryset.filter(nombre__icontains=q)
            elif campo=='Tipo':
                queryset = queryset.filter(tipoDeProducto__nombre__icontains=q)
            elif campo=='Institución':
                queryset = queryset.filter(Q(institucionProductiva__Nombre__icontains=q)|Q(institucionProductiva__NombreAbreviado__icontains=q))
            # elif campo=='Institución_Abreviado':
            #     queryset = queryset.filter(institucionProductiva__NombreAbreviado__icontains=q)

            else:
                queryset = queryset.filter(nombre__icontains=q)
        return queryset
    def get_context_data(self, *a, object_list=None, **kwargs):
        context=super().get_context_data(*a,object_list=object_list,**kwargs)
        config = ConfiguracionGeneral.get_solo()
        lcp = LocalizacionDePagina("Servicios","Lista", "Productos")
        context['config']=config
        context['lcp'] = lcp
        context['urlExportar'] = '/productos'
        context['tipos']=TipoDeProducto.objects.all()

        lista = self.get_queryset()  # self.queryset#context['object_list']

        IP=InstitucionesYProductos()
        for p in lista:
            IP.add(p)

        L=[]
        for v in IP.institucionesYProductos:
            ip=IP.institucionesYProductos[v]
            L.append({
            "latitud": ip.institucion.latitud
            , "longitud": ip.institucion.longitud
            , "textoAMostrar": ip.institucion.NombreAbreviado + " | " + " | ".join([j.nombre for j in ip.productos])
                , "url": "/instituciones_productivas/findById/" + str(ip.institucion.id)
            # +" | "+
        })


        context['listaPuntos'] = L
        #     [{
        #     "latitud": v.latitud
        #     , "longitud": v.longitud
        #     , "textoAMostrar": v.NombreAbreviado + " | " + " | ".join([j.nombre for j in v.tecnologias.all()])
        #     # +" | "+
        # } for v in IP.institucionesYProductos]
        return context


class Producto_DetailView(generic.DetailView):
    model = Producto
    def get_context_data(self, *a, object_list=None, **kwargs):
        context=super().get_context_data(*a,object_list=object_list,**kwargs)
        config = ConfiguracionGeneral.get_solo()
        lcp = LocalizacionDePagina("Servicios","Detalles", "Productos")
        context['config']=config
        context['lcp'] = lcp

        dato = context['object'].institucionProductiva
        context['listaPuntos'] = [{
            "latitud": v.latitud
            , "longitud": v.longitud
            , "textoAMostrar": v.NombreAbreviado
            , "url": "/instituciones_productivas/findById/" + str(v.id)
        } for v in [dato]]

        context['nombreProvincia'] = dato.provincia.nombre

        return context