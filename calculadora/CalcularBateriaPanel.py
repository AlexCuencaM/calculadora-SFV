import decimal
from uuid import UUID
from calculadora.models import(    
    BateriaModel,CalculoPanelModel,CalculoBateriaModel,ReporteModel
) 
class CalcularBateriaPanel:
    def __init__(self,post,token):        
        self.token = UUID(token,version=4)
        self.setPost(post)
        self.__setReporte()
        self.__setBateria()

    def setPost(self,post):
        if(post == ""):
            self.__post = self.__convertPost()
        else:
            self.__post = post

    def __convertPost(self):
        report = ReporteModel.objects.get(token=self.token)
        calculo = CalculoBateriaModel.objects.get(report=report)
        panel = CalculoPanelModel.objects.get(report=report)
        bateria = calculo.bateria
        return {
            "consumoDiario" : report.consumoDiario,
            "voltaje" : bateria.voltaje,
            "capacidad" : bateria.capacidad,
            "autonomia-dias": calculo.autonomiaDias,
            "hsp" : panel.hsp,
            "potencia-de-panel" : panel.potenciaDePanel,
        }

    def getPost(self):
        return self.__post
    def __setReporte(self):
        self.__calculo = ReporteModel(consumoDiario=decimal.Decimal(self.__post["consumoDiario"]),
            token=self.token
         )

    def __setBateria(self):
        self.__bateria = BateriaModel(voltaje=int(self.__post["voltaje"]),capacidad=int(self.__post["capacidad"]))
    def __corrienteNecesaria(self):
        try:
            result = decimal.Decimal(self.__calculo.consumoDiario/self.__bateria.voltaje)
            return result
        except ZeroDivisionError:
            return 0
        except decimal.InvalidOperation:
            return 0
        except ValueError:
            return 0

    def __setCalcularBateria(self):
        self.__calcularBateria = CalculoBateriaModel(
                bateria=self.__bateria,
                report=self.__calculo,
                corrienteNecesaria= self.__corrienteNecesaria(),
                autonomiaDias=int(self.__post["autonomia-dias"]),
            )            
#select 
    def __setCalculoPanel(self):
        if(self.__post["hsp"] == ""):
            self.__panel = CalculoPanelModel(report=self.__calculo,
                potenciaDePanel=decimal.Decimal(self.__post["potencia-de-panel"])
                )
        else:
            self.__panel = CalculoPanelModel(hsp=decimal.Decimal(self.__post["hsp"]),
                report=self.__calculo,
                potenciaDePanel=decimal.Decimal(self.__post["potencia-de-panel"])
                )

    def guardar(self):
        self.__calcularBateria.report.save()   
        self.__calcularBateria.bateria.save()     
        self.__calcularBateria.save()
        self.__panel.report.save()
        self.__panel.save()

    def calcularPanelYbateria(self):
        self.__setCalcularBateria()
        self.__setCalculoPanel()
    
    def getBateria(self):
        return self.__calcularBateria
    
    def getPanel(self):
        return self.__panel