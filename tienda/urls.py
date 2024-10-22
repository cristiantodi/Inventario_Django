from django.urls import path
from . import views

urlpatterns = [
    path('', views.tienda, name="Tienda")
    # path('categoria/<int:categoria_id>/', views.categoria, name="categoria")
]