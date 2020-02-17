from django.shortcuts import render
from django.forms import ModelForm
from django.http import HttpResponse,HttpResponseRedirect
from calculadora.models import EquipoDeComputoModel
from rest_framework import views, generics,response
from django.http import JsonResponse
from calculadora.serializers import EquipoDeComputoSerializer

class EquipoDeComputoForm(ModelForm):
    class Meta:
        model= EquipoDeComputoModel
        fields=['descripcion',]

# Create your views here.
def home(request,ventana=""):
    if(ventana=="slider"):
        return HttpResponse(render(request,'calculadora/inicio.html'))
    elif(ventana=="info"):
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

def addEquipo(request):
    if request.method =="POST":
        form = EquipoDeComputoForm(request.POST)
        if(form.is_valid()):
            form.save()
            return HttpResponseRedirect('/home')
    else:
        form = EquipoDeComputoForm()                
        return render(request,'calculadora/equipoForm.html',{'form': form})

class ListEquipoDeComputoView(generics.ListAPIView):
    queryset = EquipoDeComputoModel.objects.all()
    serializer_class = EquipoDeComputoSerializer    
    