from django.shortcuts import render,reverse
from django.forms import ModelForm
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
import json, decimal
from rest_framework import views, generics

from calculadora.models import(EquipoDeComputoModel,
    DetalleEquipoDeComputoModel,ConsumoDeDispositivo,
    BateriaModel,CalculoPanelModel,CalculoBateriaModel,ReporteModel
) 
from calculadora.serializers import EquipoDeComputoSerializer
from uuid import uuid4,UUID
from django.views.decorators.csrf import csrf_exempt

from django import forms

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

class ListEquipoDeComputoView(generics.ListAPIView):
    queryset = EquipoDeComputoModel.objects.all()
    serializer_class = EquipoDeComputoSerializer    

def getDetalle(calculos,equipo):
    return DetalleEquipoDeComputoModel(
        equipo=equipo,
        watts=int(calculos["watts"]),
        horas=decimal.Decimal(calculos["horas"])  
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
        calculos = json.loads(request.body)        
        for data in calculos["result"]:
            equipo = EquipoDeComputoModel.objects.get(pk=int(data["id"]))
            detalles = getDetalle(data,equipo)
            result = getCalculo(detalles,token)
            result.equipo.save()
            result.save(force_insert=True)
        obj = ConsumoDeDispositivo.objects.filter(token=UUID(request.session['token'],version=4))        
        total = {"total":sum([i.totalConsumoDiario for i in obj])}        
    return JsonResponse(total,safe=False)
    
def calcularPanelYbateria(request):
    if(request.method=="POST"):
        calculo = ReporteModel(consumoDiario= decimal.Decimal(request.POST["consumoDiario"]) )
        bateria = BateriaModel(voltaje=int(request.POST["voltaje"]),capacidad=int(request.POST["capacidad"]))

        calcularBateria = CalculoBateriaModel(bateria=bateria, report=calculo,
            corrienteNecesaria=decimal.Decimal(calculo.consumoDiario/bateria.voltaje), autonomiaDias=int(request.POST["autonomia-dias"]),)
        if(request.POST["hsp"] == ""):
            panel=CalculoPanelModel(report=calculo,potenciaDePanel=decimal.Decimal(request.POST["potencia-de-panel"]))

        else:
            panel=CalculoPanelModel(hsp=decimal.Decimal(request.POST["hsp"]), report=calculo,
            potenciaDePanel=decimal.Decimal(request.POST["potencia-de-panel"]))

        calcularBateria.report.save()   
        calcularBateria.bateria.save()     
        calcularBateria.save()
        panel.report.save()
        panel.save()

        devices = ConsumoDeDispositivo.objects.filter(token=UUID(request.session['token'],version=4))
        
        BA = decimal.Decimal(calcularBateria.autonomiaDias * calcularBateria.corrienteNecesaria)/ decimal.Decimal(calcularBateria.constanteDeDescarga)
        denominador = decimal.Decimal(panel.report.consumoDiario * decimal.Decimal(panel.tolerancia))
        CP = denominador / decimal.Decimal(decimal.Decimal(panel.hsp) * panel.potenciaDePanel)
        return render(request,"calculadora/reporte.html",
        {
            "devices": devices,
            "resultadosDevices": sum([i.totalConsumoDiario for i in devices]),
            "TotalBateria":round(float(BA/calcularBateria.bateria.capacidad)) ,#TB
            "TotalPanel":round(float( CP))
        })