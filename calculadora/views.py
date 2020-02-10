from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
# Create your views here.
def home(request):
    return HttpResponse(render(request,'calculadora/home.html'))
    
def info(request):
    return HttpResponse(render(request,'calculadora/ViewInformation.html'))

def botonCalcular(request):
    return HttpResponse(render(request,'calculadora/BotonCalcular.html'))

def implementacion(request):
    return HttpResponse(render(request,'calculadora/CalcularImplementacion.html'))

def contact(request):
    return HttpResponse(render(request,'calculadora/Contactar.html'))
def imagenes(request):
    return HttpResponse(render(request,'calculadora/Imagenes.html'))