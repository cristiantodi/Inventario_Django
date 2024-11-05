from django.urls import path
from . import views

urlpatterns = [
    path('', views.abonos, name="Abonos"),
]
