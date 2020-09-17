import decimal,json
from uuid import uuid4,UUID
from calculadora.CalcularCargaMax import *
from calculadora.models import(EquipoDeComputoModel,
    DetalleEquipoDeComputoModel,ConsumoDeDispositivo,    
) 
class Calcular:
    def __init__(self,request,i):
        
        self.__id = UUID(i,version=4)
        self.setDatos(request)
        self.__calcular = CalcularCargaMax(self.__datos)
    
    def setDatos(self,datos):
        if(datos == ""):
            self.__datos = self.__convertDatos()
        else:
            self.__datos = datos    
    def __resultados(self,detalleEquipo):
        return {
            "id": detalleEquipo.id,
            "descripcion": detalleEquipo.descripcion,
            "cantidad": detalleEquipo.cantidad,
            "consumoKwH": detalleEquipo.consumoKwH,
            "horarios": json.loads(detalleEquipo.horarios),

        }
    def __convertDatos(self):
        consumo = ConsumoDeDispositivo.objects.filter(token=self.getId() )                
        return {
            "result":[self.__resultados(i.equipo) for i in consumo],
        }
    def getId(self):
        return self.__id

    def __getDetalle(self,calculos,equipo):
        return DetalleEquipoDeComputoModel(
            equipo=equipo,
            descripcion = calculos["descripcion"],
            consumoKwH=Decimal(calculos["consumoKwH"]),
            cantidad=int(calculos["cantidad"]),
            horarios= json.dumps(calculos["horarios"]),
        )
    def __getCalculo(self,detalle):
        return ConsumoDeDispositivo(
            equipo=detalle,
            totalConsumoDiario = detalle.consumoKwH * detalle.cantidad,
            token= self.getId()
        )    
    #Aqui se va a modificar
    def total(self) -> dict:       
        return {"total":self.__calcular.perDay()}

    def __guardar(self,detalles):
        result = self.__getCalculo(detalles)
        result.equipo.save()
        result.save(force_insert=True)

    def guardar(self):
        for data in self.__datos["result"]:
            equipo = EquipoDeComputoModel.objects.get(pk=int(data["id"]))
            detalles = self.__getDetalle(data,equipo)                        
            self.__guardar(detalles)

    def testing(self):
        pass