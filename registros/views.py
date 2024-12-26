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

from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors

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
    form = FiltroMesAnioForm()
    mes = None
    anio = None

    if request.method == "POST":
        form = FiltroMesAnioForm(request.POST)
        if form.is_valid():
            mes = form.cleaned_data['mes']
            anio = form.cleaned_data['anio']
            # Redirigir al template con los datos filtrados
            return render(request, 'ventas_mensuales.html', {
                'form': form,
                'mes': mes,
                'anio': anio
            })

    return render(request, 'ventas_mensuales.html', {'form': form})

def generar_pdf_ventas(request, mes, anio):
    # Filtrar las ventas según el mes y el año
    ventas = Venta.objects.filter(fecha__month=mes, fecha__year=anio)

    # Calcular información adicional
    total_vendido = sum(venta.precio_unitario * venta.cantidad for venta in ventas)
    cantidad_vendida = sum(venta.cantidad for venta in ventas)

    # Crear la respuesta HTTP con el contenido del PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="ventas_{mes}_{anio}.pdf"'

    # Crear el lienzo del PDF
    pdf = canvas.Canvas(response, pagesize=letter)
    width, height = letter

    # Función para dibujar encabezado en cada página
    def draw_header():
        # Dibujar el logo
        # logo_path = "ruta/a/tu/logo.png"  # Cambia esta ruta al logo de tu empresa
        # pdf.drawImage(logo_path, 40, height - 80, width=100, height=50)  # Ajusta la posición y tamaño del logo

        # Información superior
        pdf.setFont("Helvetica-Bold", 14)
        pdf.drawString(160, height - 50, f"Reporte de Ventas - {mes}/{anio}")
        pdf.setFont("Helvetica", 12)
        pdf.drawString(40, height - 100, f"Total productos vendidos: {cantidad_vendida}")
        pdf.drawString(40, height - 120, f"Total vendido: ${total_vendido:,.2f}")

    # Preparar los datos de la tabla
    data = [["#", "Producto", "Cantidad", "Precio Unitario", "Fecha"]]  # Encabezado
    for i, venta in enumerate(ventas, start=1):
        data.append([
            i,
            venta.producto.nombre,
            venta.cantidad,
            f"${venta.precio_unitario:,.2f}",
            venta.fecha.strftime("%d/%m/%Y"),
        ])

    # Configuración de estilo de la tabla
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ])

    # Dividir la tabla en páginas
    rows_per_page = 25  # Número máximo de filas por página (ajústalo según sea necesario)
    current_row = 1

    while current_row < len(data):
        # Dibujar encabezado
        draw_header()

        # Seleccionar filas para esta página
        page_data = data[current_row:current_row + rows_per_page]

        # Crear la tabla de esta página
        table_page = Table([data[0]] + page_data, colWidths=[50, 200, 80, 100, 100])
        table_page.setStyle(style)  # Aplicar el estilo
        table_page.wrapOn(pdf, width, height)
        table_page.drawOn(pdf, 40, height - 600)  # Ajustar la posición de la tabla

        # Mover a la siguiente página
        current_row += rows_per_page
        if current_row < len(data):
            pdf.showPage()

    # Finalizar el PDF
    pdf.save()
    return response