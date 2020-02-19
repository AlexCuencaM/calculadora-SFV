from rest_framework import serializers
from calculadora.models import EquipoDeComputoModel,DetalleEquipoDeComputoModel

class EquipoDeComputoSerializer(serializers.ModelSerializer):    
    class Meta:
        model =EquipoDeComputoModel
        fields =('id','descripcion',)                
        
