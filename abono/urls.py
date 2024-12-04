from django.urls import path
from . import views

urlpatterns = [
    path('', views.creditos, name="Creditos"),
    path('crear/', views.crear_credito, name="crear"),
    path('abonar/<int:credito_id>/', views.abonar, name="abonar"), 
    path('ver_registros/<int:credito_id>/', views.ver_registros, name="ver_registros"),
]
