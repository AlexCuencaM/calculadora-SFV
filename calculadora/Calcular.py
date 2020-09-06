import decimal,json
from uuid import uuid4,UUID
from calculadora.CalcularCargaMax import *
from calculadora.models import(EquipoDeComputoModel,
    DetalleEquipoDeComputoModel,ConsumoDeDispositivo,    
) 
class Calcular:
    def __init__(self,request,id):
        self.__datos = request        
        self.__id = UUID(id,version=4)
        self.__calcular = CalcularCargaMax(self.__datos)
    def getId(self):
        return self.__id

    def __getDetalle(self,calculos,equipo):
        return DetalleEquipoDeComputoModel(
            equipo=equipo,
            descripcion = calculos["descripcion"],
            consumoKwH=int(calculos["watts"]),
            cantidad=int(calculos["cantidad"]),
            horarios= json.dumps(calculos["horarios"]),
        )
    def __getCalculo(self,detalle):
        return ConsumoDeDispositivo(
            equipo=detalle,
            totalConsumoDiario = detalle.consumoKwH*detalle.cantidad,
            token= self.getId()
        )    
    #Aqui se va a modificar
    def total(self):        
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