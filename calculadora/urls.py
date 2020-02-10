from . import views
from django.urls import path
app_name="calculadora"
urlpatterns = [
    path('home/', views.home, name="home"),
    path('info/',views.info, name="info"),
    path('calcular/',views.botonCalcular, name="botonCalcular"),
    path('implementacion/',views.implementacion, name="implementacion"),
    path('contact/',views.contact, name="contact"),
    path('imagenes/',views.imagenes, name="imagenes"),

]
