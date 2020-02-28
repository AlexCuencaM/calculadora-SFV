from . import views
from django.urls import path
app_name="calculadora"
urlpatterns = [
    path('home/', views.home, name="home"),
    path('home/<str:ventana>', views.home, name="home"),
    path('calcular/',views.botonCalcular, name="botonCalcular"),    
    path('create/equipo/',views.addEquipo, name="addEquipo"),
    path("equipos/",views.ListEquipoDeComputoView.as_view(), name="equipos"),    
    path("consumo/",views.calcularConsumoDispositivo,name="consumo"),#POST
    path("panel-y-bateria/",views.calcularPanelYbateria,name="panel-y-bateria"),
    path("reporte/<int:panel>/<int:bateria>/<str:total>/<str:inversor>/<str:ah>/<str:panelCantidad>",views.generarPdf , name="reporte"),    
]
