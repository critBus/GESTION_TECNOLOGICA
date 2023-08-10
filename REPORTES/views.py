from django.shortcuts import render,HttpResponse
from django.conf import settings
from io import BytesIO
from reportlab.pdfgen import canvas
from django.views.generic import View
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter,landscape,A4
from reportlab.lib.units import mm,cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle,Paragraph
from INSTITUCIONES_PRODUCTIVAS.models import *
from INSTITUCIONES_CIENTIFICAS.models import *

import io
from reportlab.platypus import SimpleDocTemplate, Paragraph, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Table
from django.db.models import Q
# Create your views here.
from typing import TYPE_CHECKING, Dict, List, NoReturn, Optional, Union, Tuple, cast, ClassVar

class DatosColumnaReporte:
    def __init__(self):
        self.header=""
        self.metodo_getValor=None#v->v.valor
        self.proporcion_comlumna=1
        #self.metodo_filtrar_QCampo=None#q,campo->List


class AdministradorDeReporte:
    def __init__(self):
        self.columnas:List[DatosColumnaReporte]=[]
        self.titulo=""
        self.claseModelo = None
        self.dic_campo_atributo = {}
        self.dic_campo_metodo_filtrar = {}#q,campo->List
    def setClaseModelo(self,claseModelo):
        self.claseModelo =claseModelo
        self.dic_campo_atributo={str(v):str(v) for v in vars(claseModelo)}
    def add(self,header,metodo_getValor,proporcion_comlumna=1):
        d=DatosColumnaReporte()
        d.header=header
        d.metodo_getValor=metodo_getValor
        d.proporcion_comlumna=proporcion_comlumna
        self.columnas.append(d)
        return self
    def getAction(self):
        def metodoAction(modeladmin, request, queryset):
            response = HttpResponse(content_type='application/pdf')
            buff = io.BytesIO()
            doc = SimpleDocTemplate(buff,
                                    pagesize=landscape(letter),
                                    rightMargin=40,
                                    leftMargin=40,
                                    topMargin=60,
                                    bottomMargin=18,
                                    )
            categorias = []
            styles = getSampleStyleSheet()
            header = Paragraph(self.titulo, styles['Heading1'])
            categorias.append(header)

            # ------------------
            encabezados = (v.header for v in self.columnas)

            def getL(z):
                return [v.metodo_getValor(z) for v in self.columnas]

            def p(v):
                if isinstance(v, int) \
                        or isinstance(v, float):
                    return v
                return Paragraph(
                    str(v))  # Paragraph('<font size=' + str(self.FontSise) + '>' + str(v) + "</font>")  # <center>

            # Creamos una lista de tuplas que van a contener a las personas
            detalles = [tuple(p(e) for e in getL(v))
                        for v in
                        queryset  # InstitucionProductiva.objects.all()
                        ]
            # ------------------
            # headings = ('Id', 'Descrición', 'Activo', 'Creación')

            # todascategorias = [(p.id, p.descripcion, p.activo, p.creado)for p in Categoria.objects.all().order_by('pk')]

            t = Table([encabezados] + detalles)
            t.setStyle(TableStyle(
                [
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                    ('GRID', (0, 0), (-1, -1), 1, colors.dodgerblue),
                    ('LINEBELOW', (0, 0), (-1, 0), 2, colors.darkblue),
                    ('BACKGROUND', (0, 0), (-1, 0), colors.dodgerblue)
                ]
            ))

            categorias.append(t)
            doc.build(categorias)
            response.write(buff.getvalue())
            buff.close()
            return response

        metodoAction.short_description = "Exportar a PDF"
        return metodoAction
    def getView(self):
        def metodoView(request):
            q = request.GET.get('q')
            campo = request.GET.get('campo')
            if q and campo:
                q=q.strip()
                if campo in self.dic_campo_metodo_filtrar:
                    queryset=self.dic_campo_metodo_filtrar[campo](q,campo)
                elif campo in self.dic_campo_atributo:
                    valor=self.dic_campo_atributo[campo]
                    filtro=str(valor+"__icontains")
                    queryset = self.claseModelo.objects.filter(**{filtro:q})
            else:
                queryset = self.claseModelo.objects.all()
            return self.getAction()(None,None,queryset)
        return metodoView


REPORTE_INSTITUCIONES_PRODUCTIVA_PDF=AdministradorDeReporte()
REPORTE_INSTITUCIONES_PRODUCTIVA_PDF.titulo="Instituciones Productivas"
REPORTE_INSTITUCIONES_PRODUCTIVA_PDF.add('Nombre',lambda v:v.Nombre)
REPORTE_INSTITUCIONES_PRODUCTIVA_PDF.add('Abreviado',lambda v:v.NombreAbreviado)
REPORTE_INSTITUCIONES_PRODUCTIVA_PDF.add('Contacto',lambda v:v.Contacto)
REPORTE_INSTITUCIONES_PRODUCTIVA_PDF.add('Telefono',lambda v:v.Telefono)
REPORTE_INSTITUCIONES_PRODUCTIVA_PDF.add('Correo',lambda v:v.Correo)
REPORTE_INSTITUCIONES_PRODUCTIVA_PDF.add('Provincia',lambda v:v.provincia.nombre)
REPORTE_INSTITUCIONES_PRODUCTIVA_PDF.add('Municipio',lambda v:v.municipio.nombre)
REPORTE_INSTITUCIONES_PRODUCTIVA_PDF.add('Direccion',lambda v:v.Direccion)
REPORTE_INSTITUCIONES_PRODUCTIVA_PDF.add('Institucion Productiva',lambda v:v.tipoDeInstitucionProductiva.nombre)
REPORTE_INSTITUCIONES_PRODUCTIVA_PDF.add('Refrigeracion',lambda v:v.capacidadDeRefrigeracion)
REPORTE_INSTITUCIONES_PRODUCTIVA_PDF.setClaseModelo(InstitucionProductiva)
REPORTE_INSTITUCIONES_PRODUCTIVA_PDF.dic_campo_atributo['Provincia']='provincia__nombre'
REPORTE_INSTITUCIONES_PRODUCTIVA_PDF.dic_campo_atributo['Municipio']='municipio__nombre'
REPORTE_INSTITUCIONES_PRODUCTIVA_PDF.dic_campo_atributo['Tipo']='tipoDeInstitucionProductiva__nombre'
REPORTE_INSTITUCIONES_PRODUCTIVA_PDF.dic_campo_metodo_filtrar['Producto']=lambda q,c:InstitucionProductiva.objects.filter(producto__in=Producto.objects.filter(nombre__icontains=q))




REPORTE_INSTITUCIONES_CIENTIFICA_PDF=AdministradorDeReporte()
REPORTE_INSTITUCIONES_CIENTIFICA_PDF.titulo="Instituciones Científicas"
REPORTE_INSTITUCIONES_CIENTIFICA_PDF.add('Nombre',lambda v:v.Nombre)
REPORTE_INSTITUCIONES_CIENTIFICA_PDF.add('Abreviado',lambda v:v.NombreAbreviado)
REPORTE_INSTITUCIONES_CIENTIFICA_PDF.add('Contacto',lambda v:v.Contacto)
REPORTE_INSTITUCIONES_CIENTIFICA_PDF.add('Telefono',lambda v:v.Telefono)
REPORTE_INSTITUCIONES_CIENTIFICA_PDF.add('Correo',lambda v:v.Correo)
REPORTE_INSTITUCIONES_CIENTIFICA_PDF.add('Provincia',lambda v:v.provincia.nombre)
REPORTE_INSTITUCIONES_CIENTIFICA_PDF.add('Municipio',lambda v:v.municipio.nombre)
REPORTE_INSTITUCIONES_CIENTIFICA_PDF.add('Direccion',lambda v:v.Direccion)
REPORTE_INSTITUCIONES_CIENTIFICA_PDF.add('Institucion Científica',lambda v:v.tipoDeInstitucionCientifica.nombre)
REPORTE_INSTITUCIONES_CIENTIFICA_PDF.add('Tecnologias',lambda v:"<br/>".join([z.nombre for z in v.tecnologias.all()]))
REPORTE_INSTITUCIONES_CIENTIFICA_PDF.setClaseModelo(InstitucionCientifica)
REPORTE_INSTITUCIONES_CIENTIFICA_PDF.dic_campo_atributo['Provincia']='provincia__nombre'
REPORTE_INSTITUCIONES_CIENTIFICA_PDF.dic_campo_atributo['Municipio']='municipio__nombre'
REPORTE_INSTITUCIONES_CIENTIFICA_PDF.dic_campo_atributo['Tipo']='tipoDeInstitucionCientifica__nombre'
REPORTE_INSTITUCIONES_CIENTIFICA_PDF.dic_campo_atributo['Tecnologia']='tecnologias__nombre'
#REPORTE_INSTITUCIONES_PRODUCTIVA_PDF.dic_campo_metodo_filtrar['Tecnologia']=lambda q,c:InstitucionProductiva.objects.filter(producto__in=Tecnologia.objects.filter(nombre__icontains=q))


REPORTE_TECNOLOGIAS_PDF=AdministradorDeReporte()
REPORTE_TECNOLOGIAS_PDF.titulo="Tecnologías"
REPORTE_TECNOLOGIAS_PDF.add('Nombre',lambda v:v.nombre)
REPORTE_TECNOLOGIAS_PDF.add('Accion',lambda v:v.accionEsperada)
REPORTE_TECNOLOGIAS_PDF.add('Tipo',lambda v:v.tipoDeTecnologia.nombre)#lambda v:",".join([z.nombre for z in v.tipoDeTecnologia.all()]))
REPORTE_TECNOLOGIAS_PDF.add('Especies',lambda v:"<br/>".join([z.nombreCientifico for z in v.especies.all()]))
REPORTE_TECNOLOGIAS_PDF.setClaseModelo(Tecnologia)
REPORTE_TECNOLOGIAS_PDF.dic_campo_atributo['Tipo']='tipoDeTecnologia__nombre'
REPORTE_TECNOLOGIAS_PDF.dic_campo_atributo['especie_nombreComun']='especies__nombreComun'
REPORTE_TECNOLOGIAS_PDF.dic_campo_atributo['especie_nombreCientifico']='especies__nombreCientifico'
REPORTE_TECNOLOGIAS_PDF.dic_campo_atributo['especie_tipoDeEspecie']='especies__tipoDeEspecie__nombre'


REPORTE_ESPECIES_PDF=AdministradorDeReporte()
REPORTE_ESPECIES_PDF.titulo="Especies"
REPORTE_ESPECIES_PDF.add('Nombre Común',lambda v:v.nombreComun)
REPORTE_ESPECIES_PDF.add('Nombre Científico',lambda v:v.nombreCientifico)
REPORTE_ESPECIES_PDF.add('Tipo',lambda v:v.tipoDeEspecie)#lambda v:",".join([z.nombre for z in v.tipoDeTecnologia.all()]))
REPORTE_ESPECIES_PDF.setClaseModelo(Especie)

REPORTE_PRODUCTOS_PDF=AdministradorDeReporte()
REPORTE_PRODUCTOS_PDF.titulo="Productos"
REPORTE_PRODUCTOS_PDF.add('Nombre',lambda v:v.nombre)
REPORTE_PRODUCTOS_PDF.add('Tipo',lambda v:v.tipoDeProducto.nombre)
REPORTE_PRODUCTOS_PDF.add('Institución',lambda v:v.institucionProductiva.Nombre)#lambda v:",".join([z.nombre for z in v.tipoDeTecnologia.all()]))
REPORTE_PRODUCTOS_PDF.setClaseModelo(Producto)
REPORTE_PRODUCTOS_PDF.dic_campo_atributo['Tipo']='tipoDeProducto__nombre'
# REPORTE_PRODUCTOS_PDF.dic_campo_atributo['Institución']='institucionProductiva__Nombre'
# REPORTE_PRODUCTOS_PDF.dic_campo_atributo['Institución_Abreviado']='institucionProductiva__NombreAbreviado'
REPORTE_PRODUCTOS_PDF.dic_campo_metodo_filtrar['Institución']=lambda q,c:Producto.objects.filter(Q(institucionProductiva__Nombre__icontains=q)|Q(institucionProductiva__NombreAbreviado__icontains=q))

