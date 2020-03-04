from calculadora.Calcular import *
from calculadora.Myprint import *
from calculadora.CalcularBateriaPanel import *
from calculadora.CalcularReporte import *

from django import forms
from django.shortcuts import render,reverse
from django.forms import ModelForm
from django.http import JsonResponse,FileResponse

import io
from calculadora.models import(EquipoDeComputoModel, BateriaModel,
) 

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
        category = BateriaModel.VOLTAJE     
        print(CalculoPanelModel.PROMEDIO)   
        return render(request,'calculadora/CalcularImplementacion.html',
        {
            "category":[i[0] for i in category],
            "hsp": CalculoPanelModel.PROMEDIO,          
        })
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

@csrf_exempt
def calcularConsumoDispositivo(request):     
    if(request.method == "POST"):
        calcular = Calcular(request)        
        request.session['token'] = str(calcular.getId())                
    return JsonResponse(calcular.total(),safe=False)
    
def calcularPanelYbateria(request):
    if(request.method=="POST"):
        ward = CalcularBateriaPanel(request.POST, request.session['token'])
        ward.calcularPanelYbateria()
        reporte = CalcularReporte(ward)        
        return render(request,"calculadora/reporte.html", reporte.getReporte())
        
def generarPdf(request,panel,bateria,total,inversor,ah,panelCantidad):
    buffer = io.BytesIO()
    report = MyPrint(buffer, 'A4',request.session['token'],panel,bateria,total,inversor,ah,panelCantidad)
    report.printReport()
    buffer.seek(0)    
    return FileResponse(buffer, as_attachment=True, filename='reporte.pdf')