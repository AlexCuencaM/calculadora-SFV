from calculadora.CalcularBateriaPanel import *
from calculadora.models import(    
    ConsumoDeDispositivo
) 
import decimal

class CalcularReporte:
    def __init__(self,calculoBateriaPanel):
        self.__calculoBateriaPanel = calculoBateriaPanel
        self.__setDevices()
        self.__setBA()
        self.__setCP()

    def __setDevices(self):
        self.__devices = ConsumoDeDispositivo.objects.filter(token=self.__calculoBateriaPanel.token)
    
    def __numeradorBA(self):
        return decimal.Decimal(self.__calculoBateriaPanel.getBateria().autonomiaDias * self.__calculoBateriaPanel.getBateria().corrienteNecesaria)

    def __denominadorBA(self):
        return decimal.Decimal(self.__calculoBateriaPanel.getBateria().constanteDeDescarga)

    def __setBA(self):
        self.__BA = self.__numeradorBA()/self.__denominadorBA()
     
    def __numeradorCP(self):
        return decimal.Decimal(self.__calculoBateriaPanel.getPanel().report.consumoDiario * decimal.Decimal(self.__calculoBateriaPanel.getPanel().tolerancia))

    def __denominadorCP(self):
        return decimal.Decimal(decimal.Decimal(self.__calculoBateriaPanel.getPanel().hsp) * self.__calculoBateriaPanel.getPanel().potenciaDePanel)
    
    def __setCP(self):
        self.__CP = self.__numeradorCP()/self.__denominadorCP()

    def __totalBateria(self):
        return round(float(self.__BA/self.__calculoBateriaPanel.getBateria().bateria.capacidad))

    def __totalPanel(self):
        return round(float(self.__CP))

    def getReporte(self):
        return {
            "devices": self.__devices,
            "resultadosDevices": sum([i.totalConsumoDiario for i in self.__devices]),
            "TotalBateria": self.__totalBateria(),#TB
            "TotalPanel": self.__totalPanel(),
            "inversor": self.__calculoBateriaPanel.getPost()["inversor"],
            "ah": self.__calculoBateriaPanel.getBateria().bateria.capacidad,
            "panelCantidad" : self.__calculoBateriaPanel.getPanel().potenciaDePanel,
        }