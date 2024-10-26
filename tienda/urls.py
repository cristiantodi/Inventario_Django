from django.urls import path
# from .views import sell_products
from . import views

urlpatterns = [
    path('', views.tienda, name="Tienda"),
]