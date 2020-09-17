# Devices es la lista de dispositivos por token
from decimal import Decimal


class CalcularCargaMax:
    def __init__(self, devices):
        self.__devices = devices["result"]    

    def __consumo(self, dev):
        return Decimal(dev["consumoKwH"]) * int(dev["cantidad"])

    def tabla(self):
        ConsumoPerDay = []
        for dev in self.__devices:
            ConsumoPerHour = []
            for i in range(1, 25):
                if(i in dev["horarios"]):
                    ConsumoPerHour.append(self.__consumo(dev))
                else:
                    ConsumoPerHour.append(0)
            ConsumoPerDay.append(ConsumoPerHour)              
        return ConsumoPerDay

    def perDay(self):
        tabla = self.tabla()        
        array = []
        for x in zip(*tabla):
            temp =[]
            for y in x:
                temp.append(y)
            array.append(sum(temp))        
        return max(array)

