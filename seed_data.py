import os
import random
from django.core.files import File
from django.utils import timezone
from CONFIGURACION.models import (
    ConfiguracionGeneral, PaginaPrincipal, ImagenesFondo_Principal,
    Informacion_Principal, QuienesSomos, Integrante, Provincia, Municipio
)
from INSTITUCIONES_CIENTIFICAS.models import (
    TipoDeTecnologia, Especie, Tecnologia, TipoDeInstitucionCientifica,
    InstitucionCientifica
)
from INSTITUCIONES_PRODUCTIVAS.models import (
    TipoDeInstitucionProductiva, TipoDeProducto, Producto,
    InstitucionProductiva
)

# Rutas de las imágenes
IMAGENES_BASE = 'media/seed_images/'
IMAGENES = {
    'logo': os.path.join(IMAGENES_BASE, 'logo.png'),
    'breadcrumbs': os.path.join(IMAGENES_BASE, 'breadcrumbs.png'),
    'fondo_principal': os.path.join(IMAGENES_BASE, 'fondo_principal.jpg'),
    'info_principal': os.path.join(IMAGENES_BASE, 'info_principal.jpg'),
    'quienes_somos': os.path.join(IMAGENES_BASE, 'quienes_somos.jpg'),
    'integrante': os.path.join(IMAGENES_BASE, 'integrante.jpg'),
    'tecnologia': os.path.join(IMAGENES_BASE, 'tecnologia.jpg'),
    'especie': os.path.join(IMAGENES_BASE, 'especie.jpg'),
    'institucion_cientifica': os.path.join(IMAGENES_BASE, 'institucion_cientifica.jpg'),
    'institucion_productiva': os.path.join(IMAGENES_BASE, 'institucion_productiva.jpg'),
    'producto': os.path.join(IMAGENES_BASE, 'producto.jpg'),
}

def crear_imagen(ruta):
    """Función auxiliar para crear objetos File de Django"""
    return File(open(ruta, 'rb'))

def seed_configuracion():
    """Crear datos de configuración general"""
    config = ConfiguracionGeneral.objects.create(
        nombreSitio="Gestión Tecnológica",
        linkFacebook="https://facebook.com/ejemplo",
        linkTwitter="https://twitter.com/ejemplo",
        linkYoutube="https://youtube.com/ejemplo",
        correo="contacto@ejemplo.com",
        telefono="+5355555555",
        direccion="Calle Principal #123",
        horarios="Lunes a Viernes: 8:00 - 17:00"
    )
    config.ImagenLogo.save('logo.png', crear_imagen(IMAGENES['logo']))
    config.ImagenBreadcrumbs.save('breadcrumbs.png', crear_imagen(IMAGENES['breadcrumbs']))
    config.save()

def seed_pagina_principal():
    """Crear datos de página principal"""
    pagina = PaginaPrincipal.objects.create(
        Titulo="Bienvenidos a Gestión Tecnológica",
        Descripcion="Sistema de gestión tecnológica para instituciones científicas y productivas"
    )
    
    # Crear imágenes de fondo
    for i in range(3):
        fondo = ImagenesFondo_Principal.objects.create(Pagina=pagina)
        fondo.Imagen.save(f'fondo_{i}.jpg', crear_imagen(IMAGENES['fondo_principal']))
        fondo.save()
    
    # Crear informaciones principales
    for i in range(3):
        info = Informacion_Principal.objects.create(
            Pagina=pagina,
            Titulo=f"Información Principal {i+1}",
            Descripcion=f"Descripción de la información principal {i+1}"
        )
        info.Imagen.save(f'info_{i}.jpg', crear_imagen(IMAGENES['info_principal']))
        info.save()

def seed_quienes_somos():
    """Crear datos de Quiénes Somos"""
    quienes = QuienesSomos.objects.create(
        Titulo="Quiénes Somos",
        SubTitulo="Nuestra Historia",
        Descripcion="Somos una organización dedicada a la gestión tecnológica...",
        DescripcionNuestroEquipo="Nuestro equipo está compuesto por profesionales..."
    )
    quienes.Imagen.save('quienes_somos.jpg', crear_imagen(IMAGENES['quienes_somos']))
    quienes.save()
    
    # Crear integrantes
    nombres = ["Juan Pérez", "María García", "Carlos López"]
    categorias = ["Director", "Investigador", "Técnico"]
    for i in range(3):
        integrante = Integrante.objects.create(
            Nombre=nombres[i],
            Categoria=categorias[i],
            Descripcion=f"Descripción del integrante {i+1}",
            Pagina=quienes
        )
        integrante.Imagen.save(f'integrante_{i}.jpg', crear_imagen(IMAGENES['integrante']))
        integrante.save()

def seed_ubicaciones():
    """Crear provincias y municipios"""
    provincias = ["La Habana", "Matanzas", "Villa Clara"]
    municipios = {
        "La Habana": ["Plaza", "Centro Habana", "Habana Vieja"],
        "Matanzas": ["Matanzas", "Cárdenas", "Varadero"],
        "Villa Clara": ["Santa Clara", "Remedios", "Sagua la Grande"]
    }
    
    for provincia_nombre in provincias:
        provincia = Provincia.objects.create(nombre=provincia_nombre)
        for municipio_nombre in municipios[provincia_nombre]:
            Municipio.objects.create(nombre=municipio_nombre, provincia=provincia)

def seed_tecnologias():
    """Crear tipos de tecnología y tecnologías"""
    tipos_tecnologia = ["Agrícola", "Industrial", "Informática"]
    for tipo in tipos_tecnologia:
        TipoDeTecnologia.objects.create(nombre=tipo)
    
    # Crear especies
    especies = [
        {"nombreCientifico": "Oryza sativa", "nombreComun": "Arroz", "tipoDeEspecie": "vegetal"},
        {"nombreCientifico": "Sus scrofa", "nombreComun": "Cerdo", "tipoDeEspecie": "animal"},
        {"nombreCientifico": "Zea mays", "nombreComun": "Maíz", "tipoDeEspecie": "vegetal"}
    ]
    
    for especie_data in especies:
        especie = Especie.objects.create(**especie_data)
        especie.Imagen.save(f'especie_{especie.nombreComun}.jpg', crear_imagen(IMAGENES['especie']))
        especie.save()
    
    # Crear tecnologías
    tecnologias = [
        {"nombre": "Sistema de Riego", "accionEsperada": "Optimizar el uso del agua"},
        {"nombre": "Sistema de Monitoreo", "accionEsperada": "Control de variables ambientales"},
        {"nombre": "Software de Gestión", "accionEsperada": "Automatizar procesos administrativos"}
    ]
    
    for i, tecnologia_data in enumerate(tecnologias):
        tecnologia = Tecnologia.objects.create(
            **tecnologia_data,
            tipoDeTecnologia=TipoDeTecnologia.objects.first(),
            descripcion=f"Descripción de la tecnología {i+1}"
        )
        tecnologia.Imagen.save(f'tecnologia_{i}.jpg', crear_imagen(IMAGENES['tecnologia']))
        tecnologia.save()
        tecnologia.especies.add(Especie.objects.first())

def seed_instituciones_cientificas():
    """Crear tipos de instituciones científicas e instituciones"""
    tipos = ["Centro de Investigación", "Universidad", "Laboratorio"]
    for tipo in tipos:
        TipoDeInstitucionCientifica.objects.create(nombre=tipo)
    
    # Crear instituciones científicas
    instituciones = [
        {
            "Nombre": "Centro de Investigaciones Agrícolas",
            "NombreAbreviado": "CIA",
            "latitud": 23.1353,
            "longitud": -82.3589,
            "Contacto": "Dr. Juan Pérez",
            "Telefono": "+5355555555",
            "Correo": "cia@ejemplo.com",
            "Direccion": "Calle Principal #123"
        },
        {
            "Nombre": "Instituto de Biotecnología",
            "NombreAbreviado": "IBT",
            "latitud": 23.1353,
            "longitud": -82.3589,
            "Contacto": "Dra. María García",
            "Telefono": "+5355555556",
            "Correo": "ibt@ejemplo.com",
            "Direccion": "Calle Secundaria #456"
        }
    ]
    
    for i, institucion_data in enumerate(instituciones):
        institucion = InstitucionCientifica.objects.create(
            **institucion_data,
            provincia=Provincia.objects.first(),
            municipio=Municipio.objects.first(),
            tipoDeInstitucionCientifica=TipoDeInstitucionCientifica.objects.first()
        )
        institucion.Imagen.save(f'institucion_cientifica_{i}.jpg', crear_imagen(IMAGENES['institucion_cientifica']))
        institucion.save()
        institucion.tecnologias.add(Tecnologia.objects.first())

def seed_instituciones_productivas():
    """Crear tipos de instituciones productivas, productos e instituciones"""
    tipos = ["Empresa", "Cooperativa", "Granja"]
    for tipo in tipos:
        TipoDeInstitucionProductiva.objects.create(nombre=tipo)
    
    tipos_producto = ["Agrícola", "Industrial", "Servicios"]
    for tipo in tipos_producto:
        TipoDeProducto.objects.create(nombre=tipo)
    
    # Crear productos
    productos = [
        {"nombre": "Arroz", "descripcion": "Arroz de alta calidad"},
        {"nombre": "Maíz", "descripcion": "Maíz para consumo"},
        {"nombre": "Software", "descripcion": "Software de gestión"}
    ]
    
    for i, producto_data in enumerate(productos):
        producto = Producto.objects.create(
            **producto_data,
            tipoDeProducto=TipoDeProducto.objects.first()
        )
        producto.Imagen.save(f'producto_{i}.jpg', crear_imagen(IMAGENES['producto']))
        producto.save()
    
    # Crear instituciones productivas
    instituciones = [
        {
            "Nombre": "Empresa Agrícola del Este",
            "NombreAbreviado": "EAE",
            "latitud": 23.1353,
            "longitud": -82.3589,
            "Contacto": "Ing. Carlos López",
            "Telefono": "+5355555557",
            "Correo": "eae@ejemplo.com",
            "Direccion": "Calle Industrial #789",
            "capacidadDeProductos": 1000,
            "TieneAlamacenConRefrigeracion": True
        },
        {
            "Nombre": "Cooperativa La Esperanza",
            "NombreAbreviado": "CLE",
            "latitud": 23.1353,
            "longitud": -82.3589,
            "Contacto": "Ing. Ana Martínez",
            "Telefono": "+5355555558",
            "Correo": "cle@ejemplo.com",
            "Direccion": "Carretera Central km 123",
            "capacidadDeProductos": 500,
            "TieneAlamacenConRefrigeracion": False
        }
    ]
    
    for i, institucion_data in enumerate(instituciones):
        institucion = InstitucionProductiva.objects.create(
            **institucion_data,
            provincia=Provincia.objects.first(),
            municipio=Municipio.objects.first(),
            tipoDeInstitucionProductiva=TipoDeInstitucionProductiva.objects.first()
        )
        institucion.Imagen.save(f'institucion_productiva_{i}.jpg', crear_imagen(IMAGENES['institucion_productiva']))
        institucion.save()
        institucion.productos.add(Producto.objects.first())

def run_seed():
    """Función principal para ejecutar todos los seeders"""
    print("Iniciando proceso de seed...")
    
    # Limpiar datos existentes
    print("Limpiando datos existentes...")
    ConfiguracionGeneral.objects.all().delete()
    PaginaPrincipal.objects.all().delete()
    QuienesSomos.objects.all().delete()
    Provincia.objects.all().delete()
    TipoDeTecnologia.objects.all().delete()
    TipoDeInstitucionCientifica.objects.all().delete()
    TipoDeInstitucionProductiva.objects.all().delete()
    TipoDeProducto.objects.all().delete()
    
    # Crear nuevos datos
    print("Creando nuevos datos...")
    seed_configuracion()
    seed_pagina_principal()
    seed_quienes_somos()
    seed_ubicaciones()
    seed_tecnologias()
    seed_instituciones_cientificas()
    seed_instituciones_productivas()
    
    print("Proceso de seed completado exitosamente!")

if __name__ == "__main__":
    run_seed() 