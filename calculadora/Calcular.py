import decimal
from uuid import uuid4,UUID
from calculadora.models import(EquipoDeComputoModel,
    DetalleEquipoDeComputoModel,ConsumoDeDispositivo,    
) 
class Calcular:
    def __init__(self,request,id):
        self.__datos = request        
        self.__id = UUID(id,version=4)

    def getId(self):
        return self.__id

    def __getDetalle(self,calculos,equipo):
        return DetalleEquipoDeComputoModel(
            equipo=equipo,
            descripcion = calculos["descripcion"],
            watts=int(calculos["watts"]),
            horas=decimal.Decimal(calculos["horas"])  
        )
    def __getCalculo(self,detalle):
        return ConsumoDeDispositivo(
            equipo=detalle,
            totalConsumoDiario = detalle.watts*detalle.horas,
            token= self.getId()
        )
    def __getConsumodiario(self,detalle):
        return float(detalle["watts"]) * float(detalle["horas"])

    def total(self):
        consumo = []
        for data in self.__datos["result"]:            
            consumo.append(self.__getConsumodiario(data))
        return {"total":sum([i for i in consumo])}

    def __guardar(self,detalles):
        result = self.__getCalculo(detalles)            
        result.equipo.save()
        result.save(force_insert=True)

    def guardar(self):
        for data in self.__datos["result"]:
            equipo = EquipoDeComputoModel.objects.get(pk=int(data["id"]))
            detalles = self.__getDetalle(data,equipo)                        
            self.__guardar(detalles)