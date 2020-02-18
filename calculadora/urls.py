from . import views
from django.urls import path
app_name="calculadora"
urlpatterns = [
    path('home/', views.home, name="home"),
    path('home/<str:ventana>', views.home, name="home"),
    path('calcular/',views.botonCalcular, name="botonCalcular"),    
    path('create/equipo/',views.addEquipo, name="addEquipo"),
    path("equipos/",views.ListEquipoDeComputoView.as_view(), name="equipos"),    
    path("calcular/",views.calcularConsumoDispositivo,name="calcular"),
    path("result/",views.resultCalcs,name="result"),
]
