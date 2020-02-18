from django.shortcuts import render,reverse
from django.forms import ModelForm
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
import json
from rest_framework import views, generics

from calculadora.models import(EquipoDeComputoModel,
    DetalleEquipoDeComputoModel,ConsumoDeDispositivo,
    BateriaModel,CalculoPanelModel,CalculoBateriaModel
) 
from calculadora.serializers import EquipoDeComputoSerializer
from uuid import uuid4
from django.views.decorators.csrf import csrf_exempt
class EquipoDeComputoForm(ModelForm):
    class Meta:
        model= EquipoDeComputoModel
        fields=['descripcion',]

# Create your views here.
def home(request,ventana=""):
    if(ventana=="slider"):
        return render(request,'calculadora/inicio.html')
    elif(ventana=="info"):
        return render(request,'calculadora/ViewInformation.html')
    elif(ventana=="implementacion"):
        return render(request,'calculadora/CalcularImplementacion.html')
    elif(ventana=="contact"):
        return render(request,'calculadora/Contactar.html')
    elif(ventana=="imagenes"):
        return render(request,'calculadora/Imagenes.html')
    return render(request,'calculadora/home.html')       

def botonCalcular(request):
    computoDevice = EquipoDeComputoModel.objects.all()
    return render(request,'calculadora/BotonCalcular.html',
        {"computoDevice" : computoDevice})

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

def getDetalle(calculos,equipo):
    return DetalleEquipoDeComputoModel(
        equipo=equipo,
        watts=calculos["watts"],
        horas=calculos["horas"]        
    )

def getCalculo(detalle,token):
    return ConsumoDeDispositivo(
        equipo=detalle,
        totalConsumoDiario = detalle.watts*detalle.horas,
        token=token
    )
@csrf_exempt
def calcularConsumoDispositivo(request):        
    if(request.method == "POST"):
        token = uuid4()
        request.session['token'] = str(token)
        print("hola")
        calculos = json.loads(request.body)
        print(calculos["result"])
        # for data in calculos["calculos"]:
        #     equipo = EquipoDeComputoModel.objects.get(pk=int(data["id"]))
        #     detalles = self.getDetalle(data,equipo)
        #     result = self.getCalculo(detalles,token)
        #     result.save(force_insert=True)
    return HttpResponseRedirect(reverse("calculadora:result"))
    
def resultCalcs(request):
    if(request.method == "GET"):        
        print(request.session['token'])
        total=2
        # obj = ConsumoDeDispositivo.objects.filter(token=UUID(request.session['token']))
        # total = sum([ obj.totalConsumoDiario for i in obj])            
        return render(request, 'calculadora/CalcularImplementacion.html', { 'respuesta': total,            
        })

def calcularPanelYbateria(request):
    if(request.methdo=="POST"):
        bateria = BateriaModel(request.POST["voltaje"])