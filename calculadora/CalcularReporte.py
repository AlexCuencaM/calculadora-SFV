from calculadora.CalcularBateriaPanel import *
from calculadora.models import(    
    ConsumoDeDispositivo
) 
import decimal
import math
class CalcularReporte:
    def __init__(self,calculoBateriaPanel,total):
        self.__calculoBateriaPanel = calculoBateriaPanel
        self.__setDevices()
        self.__setBA()
        self.__setCP()
        self.__total = total["total"]

    def __setDevices(self):
        self.__devices = ConsumoDeDispositivo.objects.filter(token=self.__calculoBateriaPanel.token)
    
    def __numeradorBA(self):
        return decimal.Decimal(self.__calculoBateriaPanel.getBateria().autonomiaDias * self.__calculoBateriaPanel.getBateria().corrienteNecesaria)

    def __denominadorBA(self):
        return decimal.Decimal(self.__calculoBateriaPanel.getBateria().constanteDeDescarga)

    def __setBA(self):
        self.__BA = self.__numeradorBA()/self.__denominadorBA()

    def __CDtoWatts(self):
        return self.__calculoBateriaPanel.getPanel().report.consumoDiario * 1000

    def __numeradorCP(self):#Ojo
        return decimal.Decimal(self.__CDtoWatts() * decimal.Decimal(self.__calculoBateriaPanel.getPanel().tolerancia))

    def __denominadorCP(self):
        return decimal.Decimal(decimal.Decimal(self.__calculoBateriaPanel.getPanel().hsp) * self.__calculoBateriaPanel.getPanel().potenciaDePanel)
    
    def __setCP(self):#OJO
        self.__CP = self.__numeradorCP()/self.__denominadorCP()

    def __totalBateria(self):
        result = 0
        try:
            result = math.ceil(float(self.__BA/self.__calculoBateriaPanel.getBateria().bateria.capacidad))
            return result        
        except ZeroDivisionError:
            return 0
        except decimal.InvalidOperation:
            return 0
        except ValueError:
            return 0        
    def __totalPanel(self):
        return math.ceil(float(self.__CP))

    def __cablesConectores(self):        
        return (self.__totalPanel()//2) + 1

    def getReporte(self,request):
        return {
            "devices": self.__devices,            
            "resultadosDevices": self.__total,
            "TotalBateria": self.__totalBateria(),#Ojo
            "TotalPanel": self.__totalPanel(),#Ojo
            "inversor": request.POST["inversor"],
            "ah": self.__calculoBateriaPanel.getBateria().bateria.capacidad,#Ojo
            "panelCantidad" : self.__calculoBateriaPanel.getPanel().potenciaDePanel,#Ojo
            "metro" : request.POST["metros"],
            "conector":self.__cablesConectores(),
        }    
    
