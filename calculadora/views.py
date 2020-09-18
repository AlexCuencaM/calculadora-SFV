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
        "iteracion": [i for i in range(6)],
        "panelCategory": [120,200,320]
    }

# Create your views here.
def limpiarSesion(request):
    request.session['token'] = ""
    request.session['datos'] = ""

def isClean(request):
    return request.session['datos'] == ""

def home(request,ventana=""):
    limpiarSesion(request)
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
    computoDevice = EquipoDeComputoModel.objects.order_by('id')
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
        request.session['token'] = str(uuid4())        
        request.session['datos'] = json.loads(request.body)                
        calcular = Calcular(request.session['datos'], request.session['token'])        

    return JsonResponse(calcular.total(),safe=False)

def getDatos(request,modo):    
    if(not modo):
        return ["",""]
    return [request.session['datos'], request.POST]

def initComponents(request,modo):    
    datos = getDatos(request,modo)
    calcular = Calcular(datos[0], request.session['token'])        
    ward = CalcularBateriaPanel(datos[1], request.session['token'])
    ward.calcularPanelYbateria()

    if modo:
        ward.guardar()
        calcular.guardar()
        request.session['datos'] = ""

    return CalcularReporte(ward,calcular.total())    

def calcularPanelYbateria(request):
    reporte = None
    if(not isClean(request)):        
        reporte = initComponents(request,True)        
    else:
        reporte = initComponents(request,False)
    return render(request,"calculadora/reporte.html", reporte.getReporte(request.POST))

def generarPdf(request,inversor,metro,conector,token):
    cantidades =[metro,conector]
    buffer = io.BytesIO()
    report = MyPrint(buffer, 'A4',token,inversor,cantidades)
    report.printReport()
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='reporte.pdf')