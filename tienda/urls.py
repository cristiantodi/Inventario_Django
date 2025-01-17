from django.urls import path
# from .views import sell_products
from . import views

urlpatterns = [   
    path('', views.tienda, name='Tienda'),  # URL para la página de la tienda
    path('obtener-producto/', views.obtener_producto, name='obtener_producto'),  # URL para obtener el producto
    path('vender-productos/', views.vender_productos, name='vender_productos'),  # URL para vender productos
    path('actualizar_stock/', views.actualizar_stock, name='actualizar_stock'),  # URL para actualizar productos

    path('productos/', views.lista_productos, name='lista_productos'),

    path('ventas/', views.lista_ventas, name='lista_ventas'),
    path('ventas/<int:venta_id>/', views.detalle_venta, name='detalle_venta'),
    path('ventas/<int:venta_id>/pdf/', views.generar_pdf_venta, name='generar_pdf_venta'),
]