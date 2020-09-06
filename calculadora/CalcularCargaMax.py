#Devices es la lista de dispositivos por token
from decimal import Decimal
class CalcularCargaMax:
    def __init__(self,devices):
        self.__devices = devices["result"]
    
    def __PerHour(self,dev,i):
        ConsumoPerHour = []
            if(i in dev["horarios"]):                
                ConsumoPerHour.append(self.__consumo(dev))                
        return sum(ConsumoPerHour)

    def __consumo(self,dev):
        return Decimal(Decimal(dev["consumoKwH"])  * int(dev["cantidad"]))

    def perDay(self):
        ConsumoPerDay = []
        for dev in self.__devices:
            for i in range(1,25):
                ConsumoPerDay.append(self.__PerHour(dev,i))            
        return max(ConsumoPerDay)
