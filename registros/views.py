from django.shortcuts import render
from django.db.models import Sum, F
from django.db.models.functions import TruncDate
from .models import Venta
from django.core.paginator import Paginator
import json
from django.db.models import Count
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from tienda.models import productos
from .models import Venta

from registros.models import RegistroVenta
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter


from datetime import datetime
from django.utils.timezone import now, timedelta
from django.conf import settings
from io import BytesIO
from django.http import FileResponse
from .forms import FiltroMesAnioForm
from datetime import datetime
import calendar
import os
import io

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
    # ventas = Venta.objects.all()
    ventas = Venta.objects.all().order_by('-fecha')  # Ordenar por fecha descendente
    paginator = Paginator(ventas, 20)  # Mostrar 20 registros por página

    # Obtener el número de página actual
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
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
    
    # return render(request, 'registro.html', context)
    return render(request, 'registro.html', {
        'page_obj': page_obj,
        'datos_ventas_diarias': datos_ventas_diarias,
        'datos_productos_vendidos': datos_productos_vendidos,
    })


def ventas_mensuales(request):
    if request.method == 'POST':
        form = FiltroMesAnioForm(request.POST)
        if form.is_valid():
            mes = int(form.cleaned_data['mes'])
            anio = int(form.cleaned_data['anio'])

            # Filtrar las ventas por mes y año
            ventas = Venta.objects.filter(fecha__month=mes, fecha__year=anio)

            # Si hay ventas, generar el PDF
            return generar_pdf_ventas(request, mes, anio, ventas)
    else:
        form = FiltroMesAnioForm()

    return render(request, 'ventas_mensuales.html', {'form': form})

def generar_pdf_ventas(request, mes, anio, ventas):
    # Configurar la respuesta HTTP para el PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="ventas_{mes}_{anio}.pdf"'

    # Crear un objeto canvas para generar el PDF
    c = canvas.Canvas(response, pagesize=(600, 800))

    # Agregar el logo de la empresa
    # logo_path = 'ruta/a/tu/logo.png'  # Cambia esto con la ruta de tu logo
    # c.drawImage(logo_path, 30, 750, width=100, height=50)

    # Título del PDF
    c.setFont("Helvetica", 12)
    c.drawString(200, 750, f"Ventas de {calendar.month_name[mes]} {anio}")

    # Agregar los encabezados de la tabla
    c.setFont("Helvetica-Bold", 10)
    c.drawString(30, 700, "Producto")
    c.drawString(150, 700, "Valor")
    c.drawString(250, 700, "Cantidad")
    c.drawString(350, 700, "Fecha")

    # Agregar los registros de ventas
    y_position = 680
    total_vendido = 0
    cantidad_vendida = 0

    for venta in ventas:
        if y_position < 100:  # Si la página está llena, crear una nueva página
            c.showPage()
            c.setFont("Helvetica-Bold", 10)
            c.drawString(30, 750, "Producto")
            c.drawString(150, 750, "Valor")
            c.drawString(250, 750, "Cantidad")
            c.drawString(350, 750, "Fecha")
            y_position = 730

        c.setFont("Helvetica", 10)
        c.drawString(30, y_position, venta.producto.nombre)  # Nombre del producto
        c.drawString(150, y_position, str(venta.precio_unitario))  # Precio unitario
        c.drawString(250, y_position, str(venta.cantidad))  # Cantidad vendida
        c.drawString(350, y_position, venta.fecha.strftime('%Y-%m-%d'))  # Fecha de la venta

        # Calcular totales
        total_vendido += venta.precio_unitario * venta.cantidad
        cantidad_vendida += venta.cantidad

        y_position -= 20

    # Agregar resumen con los totales
    c.setFont("Helvetica-Bold", 12)
    c.drawString(30, y_position - 20, f"Total productos vendidos: {cantidad_vendida}")
    c.drawString(30, y_position - 40, f"Total vendido: ${total_vendido:.2f}")

    # Guardar el PDF
    c.showPage()
    c.save()

    return response