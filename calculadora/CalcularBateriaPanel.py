import decimal
from uuid import UUID
from calculadora.models import(    
    BateriaModel,CalculoPanelModel,CalculoBateriaModel,ReporteModel
) 
class CalcularBateriaPanel:
    def __init__(self,post,token):
        self.__post = post
        self.token = UUID(token,version=4)
        self.__setReporte()
        self.__setBateria()
        
    def __setReporte(self):
        self.__calculo = ReporteModel(consumoDiario= decimal.Decimal(self.__post["consumoDiario"]) )) 

    def __setBateria(self):
        self.__bateria = BateriaModel(voltaje=int(self.__post["voltaje"]),capacidad=int(self.__post["capacidad"]))
    
    def __setCalcularBateria(self):
        self.__calcularBateria = CalculoBateriaModel(
                bateria=self.__bateria,
                report=self.__calculo,
                corrienteNecesaria=decimal.Decimal(self.__calculo.consumoDiario/self.__bateria.voltaje),
                autonomiaDias=int(request.POST["autonomia-dias"]),
            )    
    def __setCalculoPanel(self):
        if(self.__post["hsp"] == ""):
            self.__panel = CalculoPanelModel(report=self.__calculo,
                potenciaDePanel=decimal.Decimal(self.__post["potencia-de-panel"])
                )

        self.__panel = CalculoPanelModel(hsp=decimal.Decimal(self.__post["hsp"])
            report=self.__calculo,
            potenciaDePanel=decimal.Decimal(self.__post["potencia-de-panel"])
            )
    def __guardar(self):
        self.__calcularBateria.report.save()   
        self.__calcularBateria.bateria.save()     
        self.__calcularBateria.save()
        self.__panel.report.save()
        self.__panel.save()

    def calcularPanelYbateria(self):
        self.__setCalcularBateria()
        self.__setCalculoPanel()
        self.__guardar()