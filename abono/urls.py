from django.urls import path
from . import views

urlpatterns = [
    path('', views.abonos, name="Abonos"),
    path('crearForm/', views.crearAbono, name='crearForm'),
    # path('buscar-nombre/', views.buscar_nombre, name='buscar_nombre'),
    path('get-nombre/', views.get_nombre, name='get_nombre'),
]
