from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
# Create your views here.
def home(request,ventana=""):
    if(ventana=="info"):
        return HttpResponse(render(request,'calculadora/ViewInformation.html'))
    elif(ventana=="implementacion"):
        return HttpResponse(render(request,'calculadora/CalcularImplementacion.html'))
    elif(ventana=="contact"):
        return HttpResponse(render(request,'calculadora/Contactar.html'))
    elif(ventana=="imagenes"):
        return HttpResponse(render(request,'calculadora/Imagenes.html'))    
    return HttpResponse(render(request,'calculadora/home.html'))
       

def botonCalcular(request):
    return HttpResponse(render(request,'calculadora/BotonCalcular.html'))
