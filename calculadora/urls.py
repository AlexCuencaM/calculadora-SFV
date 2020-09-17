from . import views
from django.urls import path
app_name="calculadora"
urlpatterns = [
    path('home/', views.home, name="home"),
    path('home/<str:ventana>', views.home, name="home"),
    path('calcular/',views.botonCalcular, name="botonCalcular"),            
    path("consumo/",views.calcularConsumoDispositivo,name="consumo"),#POST
    path("panel-y-bateria/",views.calcularPanelYbateria,name="panel-y-bateria"),
    path("reporte/<str:inversor>/<str:metro>/<str:conector>/<str:token>",views.generarPdf , name="reporte"),
]
