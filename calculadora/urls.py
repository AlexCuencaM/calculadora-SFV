from . import views
from django.urls import path
app_name="calculadora"
urlpatterns = [
    path('home/', views.home, name="home"),
    path('home/<str:ventana>', views.home, name="home"),
    path('calcular/',views.botonCalcular, name="botonCalcular"),    
    path('materiales/',views.botonMateriales, name="botonMateriales"),    
    path('create/equipo/',views.addEquipo, name="addEquipo"),
    #path('create/panel/',views.addPanel, name="addPanel"),    
    path("consumo/",views.calcularConsumoDispositivo,name="consumo"),#POST
    path("panel-y-bateria/",views.calcularPanelYbateria,name="panel-y-bateria"),
    path("reporte/<int:panel>/<int:bateria>/<str:total>/<str:inversor>/<str:ah>/<str:panelCantidad>/<str:cantidad1>/<str:cantidad2>/<str:cantidad3>/<str:cantidad4>/<str:cantidad5>/<str:cantidad6>/",views.generarPdf , name="reporte"),
]
