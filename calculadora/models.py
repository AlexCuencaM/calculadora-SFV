from django.db import models
# Create your models here.
#API GET, POST
class EquipoDeComputoModel(models.Model):
    descripcion = models.CharField(max_length=255, null=False,default="NA")
    class Meta:
        ordering = ['descripcion']

#API POST
class DetalleEquipoDeComputoModel(models.Model):
    equipo = models.ForeignKey(EquipoDeComputoModel,on_delete=models.DO_NOTHING)
    descripcion = models.CharField(max_length=255, null=False,default="NA")
    consumoKwH = models.DecimalField(null=False,max_digits=5,decimal_places=2, default=0)
    cantidad = models.IntegerField(null=False,default=1)
    horarios = models.JSONField(null=True)

#API GET, POST
class ConsumoDeDispositivo(models.Model):
    equipo = models.OneToOneField(DetalleEquipoDeComputoModel, on_delete=models.CASCADE)
    totalConsumoDiario = models.DecimalField(null=False, max_digits=10, decimal_places=2)
    token = models.UUIDField()

class BateriaModel(models.Model):
    VOLTAJE =(
        (12,'12V'),(24,'24V'),(48,'48V')
    )
    voltaje = models.IntegerField(null=False, choices=VOLTAJE)
    capacidad = models.IntegerField(null=False)

class ReporteModel(models.Model):
    consumoDiario = models.DecimalField(null=False,default=0,max_digits=10, decimal_places=2)
    token = models.UUIDField()

class CalculoPanelModel(models.Model):
    PROMEDIO = 3.97
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
