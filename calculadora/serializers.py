from rest_framework import serializers
from calculadora.models import EquipoDeComputoModel,DetalleEquipoDeComputoModel

class DetalleDeEquipoDeComputoSerializer(serializers.ModelSerializer):
    class Meta:
        model=DetalleEquipoDeComputoModel
        fields=('watts', 'horas')

class EquipoDeComputoSerializer(serializers.ModelSerializer):    
    class Meta:
        model =EquipoDeComputoModel
        fields =('descripcion',)        
        
