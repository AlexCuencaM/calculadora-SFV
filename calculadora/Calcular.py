import json,decimal
from uuid import uuid4,UUID
from calculadora.models import(EquipoDeComputoModel,
    DetalleEquipoDeComputoModel,ConsumoDeDispositivo,    
) 
class Calcular:
    def __init__(self,request):
        self.__datos = json.loads(request.body)        
        self.__id = uuid4()

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

    def total(self):
        for data in self.__datos["result"]:
            equipo = EquipoDeComputoModel.objects.get(pk=int(data["id"]))
            detalles = self.__getDetalle(data,equipo)
            result = self.__getCalculo(detalles)            
            result.equipo.save()

            result.save(force_insert=True)
        obj = ConsumoDeDispositivo.objects.filter(token=self.getId())

        return {"total":sum([i.totalConsumoDiario for i in obj])}
