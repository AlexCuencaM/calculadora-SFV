from django.shortcuts import render,reverse
from django.forms import ModelForm
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
import json
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
        return render(request,'calculadora/CalcularImplementacion.html',{"category":[i[0] for i in category]})
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
        horas=float(calculos["horas"])  
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
    
# def resultCalcs(request):
#     if(request.method == "GET"):
#         print("GET ", request.session['token'])
#         total=2
#         # )
#         # total = sum([ obj.totalConsumoDiario for i in obj])            
#         return render(request, 'calculadora/CalcularImplementacion.html', { 'respuesta': total,            
#         })

def calcularPanelYbateria(request):
    if(request.methdod=="POST"):
        calculo = ReporteModel(consumoDiario= float(request.POST["consumo-diario"]) )
        bateria = BateriaModel(voltaje=int(request.POST["voltaje"]),capacidad=int(request.POST["capacidad"]))
        calcularBateria = CalculoBateriaModel(bateria=bateria, report=calculo,
            corrienteNecesaria=float(bateria.capacidad/bateria.voltaje), autonomiaDias=int(request.POST["autonomia-dias"]),)
        panel=CalculoPanelModel(hsp=float(request.POST["hsp"]), report=calculo,
            potenciaDePanel=request.POST["potencia-de-panel"])
        # calculo.save()
        # calcularBateria.save()
        panel.save(force_insert=True)
        obj = ConsumoDeDispositivo.objects.filter(token=UUID(request.session['token']))
        return render(request,"calculadora/reporte.html",
        {
            "devices": obj,
            "resultadosDevices": sum([obj.totalConsumoDiario for i in obj]),
            "TotalBateria":float((calcularBateria.autonomiaDias*calcularBateria.corrienteNecesaria)/calcularBateria.constanteDeDescarga)  ,
            "TotalPanel":float((panel.report.consumoDiario*panel.tolerancia)/(panel.hsp*panel.potenciaDePanel) ),
        })
