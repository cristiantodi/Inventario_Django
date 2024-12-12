from django.urls import path
from . import views

urlpatterns = [
    path('ventas/', views.registro_ventas, name='registro_ventas'),
    path('registrar-venta/', views.registrar_venta, name='registrar_venta'),
]