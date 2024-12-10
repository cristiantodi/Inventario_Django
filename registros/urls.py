from django.urls import path
from . import views

urlpatterns = [
    path('', views.graficar_ventas, name='Registro'),
]