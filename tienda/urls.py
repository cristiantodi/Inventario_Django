from django.urls import path
# from .views import sell_products
from . import views

urlpatterns = [   
    path('productos/', views.lista_productos, name='lista_productos'),

    path('', views.tienda, name='Tienda'),  # URL para la página de la tienda
    path('obtener-producto/', views.obtener_producto, name='obtener_producto'),  # URL para obtener el producto
    path('vender-productos/', views.vender_productos, name='vender_productos'),  # URL para vender productos
    path('actualizar_stock/', views.actualizar_stock, name='actualizar_stock'),
]