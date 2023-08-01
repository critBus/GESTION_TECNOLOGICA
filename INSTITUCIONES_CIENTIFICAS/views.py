from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from .models import *
import os
def rellenar_instituciones_productivas(request):
    class LT:
        def __init__(self):
            self.lt = TipoDeInstitucionCientifica.objects.all()
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

        p=InstitucionCientifica()
        p.Direccion="dire "+str(i)
        p.NombreAbreviado="Abre "+str(i)
        p.tecnologias=10+i
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