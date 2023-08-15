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
