from django.urls import path
from . import views

urlpatterns = [
    path('ventas/', views.registro_ventas, name='registro_ventas'),
    path('registrar-venta/', views.registrar_venta, name='registrar_venta'),
    path('ventas/mensuales/', views.ventas_mensuales, name='ventas_mensuales'),
    path('ventas/mensuales/pdf/<int:mes>/<int:anio>/', views.generar_pdf_ventas, name='generar_pdf_ventas'),
]