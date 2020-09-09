from calculadora.Calcular import *
from calculadora.Myprint import *
from calculadora.CalcularBateriaPanel import *
from calculadora.CalcularReporte import *

from django import forms
from django.shortcuts import render,reverse
from django.forms import ModelForm
from django.http import JsonResponse,FileResponse,HttpResponseRedirect

import io,json
from calculadora.models import(EquipoDeComputoModel, BateriaModel,CalculoPanelModel
) 

from django.views.decorators.csrf import csrf_exempt
class EquipoDeComputoForm(ModelForm):
    class Meta:
        model= EquipoDeComputoModel
        fields=['descripcion',]
def detalles():    
    return {
        "category":[i[0] for i in BateriaModel.VOLTAJE],
        "hsp": CalculoPanelModel.PROMEDIO,
        "iteracion": [i for i in range(6)]
    }

# Create your views here.
def home(request,ventana=""):
    if(ventana=="slider"):
        return render(request,'calculadora/inicio.html')
    elif(ventana=="info"):
        return render(request,'calculadora/ViewInformation.html')
    elif(ventana=="implementacion"):        
        return render(request,'calculadora/CalcularImplementacion.html',detalles())
    elif(ventana=="contact"):
        return render(request,'calculadora/Contactar.html')
    elif(ventana=="imagenes"):
        return render(request,'calculadora/imagenes.html')
    return render(request,'calculadora/home.html')       

def botonCalcular(request):
    computoDevice = EquipoDeComputoModel.objects.all()
    return render(request,'calculadora/BotonCalcular.html',
        {"computoDevice" : computoDevice})
def botonMateriales(request):
    return render(request,'calculadora/BotonMaterial.html',
        {"iteracion": [i for i in range(6)]})

def addEquipo(request):
    if request.method =="POST":
        form = EquipoDeComputoForm(request.POST)
        if(form.is_valid()):
            form.save()
            return HttpResponseRedirect('/home')
    else:
        form = EquipoDeComputoForm()                
        return render(request,'calculadora/equipoForm.html',{'form': form})

#Mucho OJO aqui es :D
@csrf_exempt
def calcularConsumoDispositivo(request):     
    if(request.method == "POST"):        
        request.session['token'] = str(uuid4())        
        request.session['datos'] = json.loads(request.body)                
        calcular = Calcular(request.session['datos'], request.session['token'])        

    return JsonResponse(calcular.total(),safe=False)
    
def calcularPanelYbateria(request):
    if(request.method=="POST"):        
        calcular = Calcular(request.session['datos'], request.session['token'])
        calcular.guardar()
        ward = CalcularBateriaPanel(request.POST, request.session['token'])
        ward.calcularPanelYbateria()
        reporte = CalcularReporte(ward,calcular.total())        
        
    return render(request,"calculadora/reporte.html", reporte.getReporte(request))
        
def generarPdf(request,panel,bateria,total,inversor,ah,panelCantidad):
    buffer = io.BytesIO()
    report = MyPrint(buffer, 'A4',request.session['token'],panel,bateria,total,inversor,ah,panelCantidad)
    report.printReport()
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='reporte.pdf')