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

import io
from reportlab.platypus import SimpleDocTemplate, Paragraph, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Table

# Create your views here.
from typing import TYPE_CHECKING, Dict, List, NoReturn, Optional, Union, Tuple, cast, ClassVar

class DatosColumnaReporte:
    def __init__(self):
        self.header=""
        self.metodo_getValor=None#v->v.valor
        self.proporcion_comlumna=1

class AdministradorDeReporte:
    def __init__(self):
        self.columnas:List[DatosColumnaReporte]=[]
        self.titulo=""
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
REPORTE_INSTITUCIONES_CIENTIFICA_PDF.add('Institucion Productiva',lambda v:v.tipoDeInstitucionCientifica.nombre)
REPORTE_INSTITUCIONES_CIENTIFICA_PDF.add('Tecnologias',lambda v:",".join([z.nombre for z in v.tecnologias.all()]))


REPORTE_TECNOLOGIAS_PDF=AdministradorDeReporte()
REPORTE_TECNOLOGIAS_PDF.titulo="Tecnologías"
REPORTE_TECNOLOGIAS_PDF.add('Nombre',lambda v:v.nombre)
REPORTE_TECNOLOGIAS_PDF.add('Accion',lambda v:v.accionEsperada)
REPORTE_TECNOLOGIAS_PDF.add('Tipo',lambda v:v.tipoDeTecnologia.nombre)#lambda v:",".join([z.nombre for z in v.tipoDeTecnologia.all()]))


#
# def reporte_INSTITUCIONES_PRODUCTIVA_PDF(modeladmin, request, queryset):
#
#
#     response = HttpResponse(content_type='application/pdf')
#     buff = io.BytesIO()
#     doc = SimpleDocTemplate(buff,
#                             pagesize=landscape(letter),
#                             rightMargin=40,
#                             leftMargin=40,
#                             topMargin=60,
#                             bottomMargin=18,
#                             )
#     categorias = []
#     styles = getSampleStyleSheet()
#     header = Paragraph("Listado de Categorías", styles['Heading1'])
#     categorias.append(header)
#
#
#     #------------------
#     encabezados = ('Nombre', 'Abreviado'
#                    , 'Contacto', 'Telefono', 'Correo', 'Provincia'
#                    , 'Municipio', 'Direccion', 'Institucion Productiva'
#                    , 'Refrigeracion'
#                    )
#
#     def getL(v):
#         return [v.Nombre, v.NombreAbreviado
#             , v.Contacto, v.Telefono, v.Correo, v.provincia.nombre
#             , v.municipio.nombre, v.Direccion
#             , v.tipoDeInstitucionProductiva.nombre
#             , v.capacidadDeRefrigeracion]
#
#     def p(v):
#         if isinstance(v, int) \
#                 or isinstance(v, float):
#             return v
#         return Paragraph(str(v))#Paragraph('<font size=' + str(self.FontSise) + '>' + str(v) + "</font>")  # <center>
#
#     # Creamos una lista de tuplas que van a contener a las personas
#     detalles = [tuple(p(e) for e in getL(v))
#                 for v in
#                 queryset#InstitucionProductiva.objects.all()
#                 ]
#     #------------------
#     #headings = ('Id', 'Descrición', 'Activo', 'Creación')
#
#     #todascategorias = [(p.id, p.descripcion, p.activo, p.creado)for p in Categoria.objects.all().order_by('pk')]
#
#     t = Table([encabezados] + detalles)
#     t.setStyle(TableStyle(
#         [
#             ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
#             ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
#             ('GRID', (0, 0), (-1, -1), 1, colors.dodgerblue),
#             ('LINEBELOW', (0, 0), (-1, 0), 2, colors.darkblue),
#             ('BACKGROUND', (0, 0), (-1, 0), colors.dodgerblue)
#         ]
#     ))
#
#     categorias.append(t)
#     doc.build(categorias)
#     response.write(buff.getvalue())
#     buff.close()
#     return response
#
# reporte_INSTITUCIONES_PRODUCTIVA_PDF.short_description = "Exportar a PDF"



# class Reporte_INSTITUCIONES_PRODUCTIVA_PDF(View):
#
#
#
#
#     def cx(self,v):
#         return v#self.Ancho-
#     def cy(self,v):
#         #print(self.Alto-v)
#         return self.Alto-v
#
#     def cabecera(self, pdf):
#         # Utilizamos el archivo logo_django.png que está guardado en la carpeta media/imagenes
#         archivo_imagen = settings.MEDIA_ROOT + '/logo/logo.png'
#         # Definimos el tamaño de la imagen a cargar y las coordenadas correspondientes
#         #pdf.drawImage(archivo_imagen, 40, 750, 120, 90, preserveAspectRatio=True)
#         pdf.drawImage(archivo_imagen, self.cx(40), self.cy(100), 120, 90, preserveAspectRatio=True)
#         # Establecemos el tamaño de letra en 16 y el tipo de letra Helvetica
#         pdf.setFont("Helvetica", 16)
#         # Dibujamos una cadena en la ubicación X,Y especificada
#         pdf.drawString(self.cx(230), self.cy(60), u"PYTHON PIURA")
#         pdf.setFont("Helvetica", 14)
#         pdf.drawString(self.cx(200), self.cy(80), u"REPORTE DE PERSONAS")
#
#
#
#     def get(self, request, *args, **kwargs):
#         self.Ancho=800
#         self.Alto=600
#         self.FontSise=8
#
#         #Indicamos el tipo de contenido a devolver, en este caso un pdf
#         response = HttpResponse(content_type='application/pdf')
#         #La clase io.BytesIO permite tratar un array de bytes como un fichero binario, se utiliza como almacenamiento temporal
#         buffer = BytesIO()
#         #Canvas nos permite hacer el reporte con coordenadas X y Y
#         pdf = canvas.Canvas(buffer)
#
#
#         #pdf.setPageSize(landscape(A4))
#         #Llamo al método cabecera donde están definidos los datos que aparecen en la cabecera del reporte.
#         #self.cabecera(pdf)
#         #y = 600
#         self.tabla(pdf)
#         #Con show page hacemos un corte de página para pasar a la siguiente
#         pdf.showPage()
#         pdf.save()
#         pdf = buffer.getvalue()
#         buffer.close()
#         response.write(pdf)
#         return response
#
#     def tabla(self, pdf):
#         # Creamos una tupla de encabezados para neustra tabla
#         encabezados = ('Nombre', 'Abreviado'
#                        , 'Contacto', 'Telefono','Correo','Provincia'
#                        ,'Municipio','Direccion','Institucion Productiva'
#                        ,'Refrigeracion'
#                        )
#         def getL(v):
#             return [v.Nombre,v.NombreAbreviado
#                      ,v.Contacto,v.Telefono,v.Correo,v.provincia.nombre
#                      ,v.municipio.nombre,v.Direccion
#                      ,v.tipoDeInstitucionProductiva.nombre
#                      ,v.capacidadDeRefrigeracion]
#         def p(v):
#             if isinstance(v,int)\
#                 or isinstance(v,float):
#                 return v
#             return Paragraph('<font size='+str(self.FontSise)+'>'+str(v)+"</font>")#<center>
#
#         # Creamos una lista de tuplas que van a contener a las personas
#         detalles = [ tuple( p(e) for e in getL(v))
#                     for v in
#                     InstitucionProductiva.objects.all()]
#         # Establecemos el tamaño de cada una de las columnas de la tabla
#         anchoGeneral=(self.Ancho-(40*2))/len(encabezados)
#         anchosDeColumnas=[anchoGeneral for i in range(len(encabezados))]
#         anchosDeColumnas[-1]=anchosDeColumnas[-1]*0.8
#         anchosDeColumnas[-2] = anchosDeColumnas[-2] * 1.2
#         detalle_orden = Table([encabezados] + detalles
#                               , colWidths=anchosDeColumnas)#, colWidths=[2 * cm, 5 * cm, 5 * cm, 5 * cm]
#         # Aplicamos estilos a las celdas de la tabla
#         detalle_orden.setStyle(TableStyle(
#             [
#                 # La primera fila(encabezados) va a estar centrada
#                 ('ALIGN', (0, 0), (-1,-1), 'CENTER'),
#                 ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
#                 # Los bordes de todas las celdas serán de color negro y con un grosor de 1
#                 ('GRID', (0, 0), (-1, -1), 1, colors.black),
#                 # El tamaño de las letras de cada una de las celdas será de 10
#                 ('FONTSIZE', (0, 0), (-1, -1), self.FontSise),
#             ]
#         ))
#         # Establecemos el tamaño de la hoja que ocupará la tabla
#         detalle_orden.wrapOn(pdf, 800, 400)
#         # Definimos la coordenada donde se dibujará la tabla
#         detalle_orden.drawOn(pdf, self.cx(60), self.cy(200))#450