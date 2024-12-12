from django.shortcuts import render
from django.db.models import Sum, F
from registros.models import RegistroVenta
from django.utils import timezone
from django.utils.timezone import now, timedelta
import json
from datetime import datetime, timedelta

from tienda.models import productos
from .models import Venta
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

from django.db.models.functions import TruncDate
from django.db.models import Count

# def graficar_ventas(request):
#     # Filtrar las ventas de los últimos 7 días
#     hoy = timezone.now()  # Ahora con soporte de zona horaria
#     hace_una_semana = hoy - timedelta(days=7)

#     ventas = RegistroVenta.objects.filter(fecha__range=[hace_una_semana, hoy])

#     # Agrupar por día y sumar valores
#     ventas_por_dia = ventas.extra(select={'day': "DATE(fecha)"}).values('day').annotate(total=Sum('valor'))

#     contexto = {
#         'ventas_por_dia': ventas_por_dia,
#     }
#     return render(request, 'registro.html', contexto)

# def graficar_ventas(request):
#     hoy = now()
#     hace_una_semana = hoy - timedelta(days=7)

#     ventas = RegistroVenta.objects.filter(fecha__range=[hace_una_semana, hoy])
#     ventas_por_dia = (
#         ventas.extra(select={'day': "DATE(fecha)"})
#         .values('day')
#         .annotate(total=Sum('valor'))
#     )

#     # Convierte ventas_por_dia a JSON serializable
#     ventas_por_dia_json = json.dumps(list(ventas_por_dia))

#     contexto = {
#         'ventas_por_dia': ventas_por_dia_json,  # Enviar JSON serializado al template
#     }
#     return render(request, 'registro.html', contexto)

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