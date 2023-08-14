from django.shortcuts import render

# Create your views here.
from .models import *
# Create your views here.
from GESTION_TECNOLOGICA.Utiles.LocalizacionDePagina import *
from INSTITUCIONES_PRODUCTIVAS.models import *
from INSTITUCIONES_CIENTIFICAS.models import *
def view_home(request):

    config = ConfiguracionGeneral.get_solo()
    datos = PaginaPrincipal.get_solo()
    return render(request,'visualCliente/home.html', {
        'config': config
        ,"datos":datos
        ,"listaFondos":ImagenesFondo_Principal.objects.filter(Pagina=datos)
        ,"listaInformaciones":Informacion_Principal.objects.filter(Pagina=datos)

    })

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