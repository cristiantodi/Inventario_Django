from django.shortcuts import render
from django.db.models import Sum, F
from django.db.models.functions import TruncDate
from .models import Venta
import json
from django.db.models import Count
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from tienda.models import productos
from .models import Venta

@csrf_exempt
def registrar_venta(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            for item in data:
                producto = productos.objects.get(id=item['producto_id'])
                
                # Crear registro de venta
                Venta.objects.create(
                    producto=producto,
                    cantidad=item['cantidad'],
                    precio_unitario=item['precio_unitario'],
                    total_venta=item['cantidad'] * item['precio_unitario']
                )
            
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    return JsonResponse({'error': 'Método no permitido'}, status=405)

def registro_ventas(request):
    # Obtener ventas
    ventas = Venta.objects.all()
    
    # Preparar datos para gráfico de ventas diarias
    ventas_diarias = (Venta.objects
        .annotate(fecha_venta=TruncDate('fecha'))
        .values('fecha_venta')
        .annotate(total_ventas=Sum('total_venta'))
        .order_by('fecha_venta')
    )
    
    # Preparar datos para gráfico de productos más vendidos
    productos_mas_vendidos = (Venta.objects
        .values('producto__nombre')
        .annotate(cantidad_total=Sum('cantidad'))
        .order_by('-cantidad_total')[:10]
    )
    
    # Convertir datos para gráficos
    datos_ventas_diarias = json.dumps([
        {
            'fecha': str(venta['fecha_venta']), 
            'total_ventas': float(venta['total_ventas'])
        } for venta in ventas_diarias
    ])
    
    datos_productos_vendidos = json.dumps([
        {
            'producto': producto['producto__nombre'], 
            'cantidad': producto['cantidad_total']
        } for producto in productos_mas_vendidos
    ])
    
    context = {
        'ventas': ventas,
        'datos_ventas_diarias': datos_ventas_diarias,
        'datos_productos_vendidos': datos_productos_vendidos
    }
    
    return render(request, 'registro.html', context)