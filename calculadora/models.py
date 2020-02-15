from django.db import models
#from uuid import uuid4 default=uuid4()

# Create your models here.
#API GET, PUT, PATCH
class EquipoDeComputoModel(models.Model):
    descripcion = models.CharField(max_length=255, null=False)
    watts = models.IntegerField(null=False)
    horas = models.DecimalField(null=False, max_digits=10, decimal_places=2)

#API GET, POST
class ConsumoDeDispositivo(models.Model):
    equipo = models.OneToOneField(EquipoDeComputoModel, on_delete=models.CASCADE)
    totalConsumoDiario = models.DecimalField(null=False, max_digits=10, decimal_places=2)
    token = models.UUIDField(null=False)

class BateriaModel(models.Model):
    VOLTAJE =(
        (12,'12V'),(24,'24V'),(48,'48V')
    )
    voltaje = models.IntegerField(null=False, choices=VOLTAJE)
    capacidad = models.IntegerField(null=False)

class ReporteModel(models.Model):
    consumoDiario = models.DecimalField(null=False,default=0,max_digits=10, decimal_places=2)

class CalculoPanelModel(models.Model):
    PROMEDIO = 3.18
    TOLERANCIA = 1.3
    hsp = models.DecimalField(null=False, max_digits=10, decimal_places=2, default=PROMEDIO)
    potenciaDePanel = models.DecimalField(null=False, max_digits=10, decimal_places=2,default=1)
    tolerancia = models.DecimalField(null=False, default=TOLERANCIA, max_digits=10, decimal_places=2)
    report = models.OneToOneField(ReporteModel, on_delete=models.CASCADE)


class CalculoBateriaModel(models.Model):
    CONSTANTE = 0.7
    bateria = models.OneToOneField(BateriaModel, on_delete=models.CASCADE)
    corrienteNecesaria = models.DecimalField(null=False, max_digits=10, decimal_places=2)
    autonomiaDias = models.IntegerField(null=False,default=1)
    constanteDeDescarga = models.DecimalField(null=False, default=CONSTANTE, max_digits=10, decimal_places=2)
    report = models.OneToOneField(ReporteModel, on_delete=models.CASCADE)


