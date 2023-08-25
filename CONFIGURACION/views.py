from django.shortcuts import render

# Create your views here.
from .models import *
# Create your views here.
from GESTION_TECNOLOGICA.Utiles.LocalizacionDePagina import *
from GESTION_TECNOLOGICA.Utiles.UtilesGenerales import *
from INSTITUCIONES_PRODUCTIVAS.models import *
from INSTITUCIONES_CIENTIFICAS.models import *


from builtins import KeyError
def seguridadError(vista):
    def zz(*args,**keywords):
        try:
            return vista(*args,**keywords)

        except:

            verException()
            lcp = LocalizacionDePagina("Advertencia", "Error en url")

            return render(args[0], 'visualCliente/error_500.html',
                          {"lcp": lcp})

    return zz

def vistaErrorUrl(request):
    lcp = LocalizacionDePagina("Advertencia", "Error 404")

    return render(request, 'visualCliente/error_404.html',
                           {"lcp": lcp}
                           )

@seguridadError
def view_home(request):

    config = ConfiguracionGeneral.get_solo()
    datos = PaginaPrincipal.get_solo()
    return render(request,'visualCliente/home.html', {
        'config': config
        ,"datos":datos
        ,"listaFondos":ImagenesFondo_Principal.objects.filter(Pagina=datos)
        ,"listaInformaciones":Informacion_Principal.objects.filter(Pagina=datos)

    })
@seguridadError
def view_quienes_somos(request):
    lcp = LocalizacionDePagina("Informacíon", "Quienes Somos")
    config = ConfiguracionGeneral.get_solo()
    datos = QuienesSomos.get_solo()
    return render(request,'visualCliente/quienes_somos.html', {
        'config': config
        , "lcp": lcp
        ,"datos":datos
        ,"cantidad_insitituciones_productivas":InstitucionProductiva.objects.all().count()
        , "cantidad_insitituciones_cientificas": InstitucionCientifica.objects.all().count()
        , "cantidad_productos": Producto.objects.all().count()
        , "cantidad_tecnologias": Tecnologia.objects.all().count()

    })

class ImagenEnGaleria:
    def __init__(self):
        self.tag=""
        self.tag_titulo=None
        self.Imagen=None
        self.url=""
        self.id=""
        self.titulo=""
        self.descripcion=""
class EtiquetaYTitulo:
    def __init__(self):
        self.tag = ""
        self.tag_titulo = None

@seguridadError
def view_galeria(request):
    lcp = LocalizacionDePagina("Informacíon", "Galería")
    config = ConfiguracionGeneral.get_solo()
    datos:List[ImagenEnGaleria] = []
    listaEtiquetas=[]
    listaEtiquetasYTitulos=[]

    def addImgs(l,url,tag,tag_titulo=None):#,attrib_descripcion="descripcion"
        for v in l:
            if v.Imagen:
                img=ImagenEnGaleria()
                img.Imagen=v.Imagen
                img.url=url+str(v.id)
                img.id=v.id
                img.tag=tag
                img.titulo=str(v)
                img.descripcion=v.descripcion#getattr(v,attrib_descripcion)
                img.tag_titulo=tag_titulo if tag_titulo else tag
                datos.append(img)
                if not tag in listaEtiquetas:
                    listaEtiquetas.append(tag)
                    e=EtiquetaYTitulo()
                    e.tag=img.tag
                    e.tag_titulo=img.tag_titulo
                    listaEtiquetasYTitulos.append(e)



    addImgs(InstitucionProductiva.objects.all(),"/instituciones_productivas/findById/"
            ,"instituciones_productivas","Instituciones Productivas")
    addImgs(InstitucionCientifica.objects.all(), "/instituciones_tecnologicas/findById/"
            , "instituciones_tecnologicas","Instituciones Tecnológicas")
    addImgs(Producto.objects.all(), "/Servicios/Productos/findById/", "Productos")
    addImgs(Tecnologia.objects.all(), "/Servicios/Tecnologias/findById/", "Tecnologias")
    addImgs(Especie.objects.all(), "/Servicios/Especies/findById/", "Especies")


    return render(request,'visualCliente/Galeria.html', {
        'config': config
        , "lcp": lcp
        ,"datos":datos
        ,"listaEtiquetasYTitulos":listaEtiquetasYTitulos


    })