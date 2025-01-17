from django.shortcuts import render, get_object_or_404, redirect
from .models import productos, Venta
from django.http import JsonResponse, HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
import logging
from django.template.loader import get_template
from xhtml2pdf import pisa
from io import BytesIO

# Create your views here.

def tienda(request):
    # Opcionalmente, puedes pasar productos si deseas mostrar algunos inicialmente
    producto = productos.objects.all()
    return render(request, 'tienda.html', {'producto': producto})

# ----------------------------------------TIENDA------------------------------------------------------
def obtener_producto(request):
    producto_id = request.GET.get('buscar')
    producto = get_object_or_404(productos, id=producto_id)
    
    # Crear una respuesta JSON con los datos del producto
    response_data = {
        'id': producto.id,
        'nombre': producto.nombre,
        'imagen_url': producto.imagen.url if producto.imagen else '',
        'contenido': producto.contenido,
        'precio': producto.precio,
        'stock': producto.cantidad,
    }
    
    return JsonResponse(response_data)

# -------------------------------------------------------------
logger = logging.getLogger(__name__)
@csrf_exempt
def vender_productos(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            logger.info(f'Datos recibidos: {data}')
            total_venta = 0
            detalles_productos = []
            
            with transaction.atomic():
                for id, producto in data.items():
                    try:
                        prod = productos.objects.get(id=id)
                    except productos.DoesNotExist:
                        logger.error(f'Producto con ID {id} no encontrado')
                        return JsonResponse({'error': f'Producto con ID {id} no encontrado'}, status=404)
                    
                    cantidad_vendida = producto.get('cantidad', 0)
                    if prod.cantidad < cantidad_vendida:
                        logger.warning(f'Stock insuficiente para el producto {prod.nombre}')
                        return JsonResponse({'error': f'Stock insuficiente para el producto {prod.nombre}'}, status=400)

                    # Calcular subtotal y actualizar total
                    subtotal = prod.precio * cantidad_vendida
                    total_venta += subtotal

                    # Guardar detalles del producto
                    detalles_productos.append({
                        'id': prod.id,
                        'nombre': prod.nombre,
                        'contenido': prod.contenido,
                        'precio_unitario': prod.precio,
                        'cantidad': cantidad_vendida,
                        'subtotal': subtotal
                    })

                    prod.cantidad -= cantidad_vendida
                    prod.save()
                    logger.info(f'Venta registrada para producto {prod.nombre}')

                # Crear el registro de venta
                venta = Venta.objects.create(
                    total=total_venta,
                    detalles=detalles_productos
                )
                logger.info(f'Venta #{venta.id} creada exitosamente')
            
            return JsonResponse({'status': 'success', 'venta_id': venta.id})
        except Exception as e:
            logger.error(f'Error inesperado: {str(e)}')
            return JsonResponse({'error': f'Ocurrió un error inesperado: {str(e)}'}, status=500)
    return JsonResponse({'error': 'Método no permitido'}, status=405)

# ----------------------------------------INVENTARIO------------------------------------------------------
def lista_productos(request):
    query = request.GET.get('query')
    productos_list = productos.objects.all()

    # Verificar si hay una consulta de búsqueda
    if query:
        try:
            # Si la consulta es un número, buscar por ID
            producto_id = int(query)
            productos_list = productos_list.filter(id=producto_id)
        except ValueError:
            # Si no es un número, buscar por nombre
            productos_list = productos_list.filter(nombre__icontains=query)

    # Manejo de incremento o decremento de la cantidad temporal
    return render(request, 'inventario.html', {'productos': productos_list})

# ----------------------------------------------------------------------------
def actualizar_stock(request):
    if request.method == "POST":
        try:
            datos = json.loads(request.body)
            cambios = datos.get('cambios', [])

            for cambio in cambios:
                producto_id = cambio['id']
                cantidad_cambio = cambio['cantidad']

                # Actualizar el producto en la base de datos
                try:
                    producto = productos.objects.get(id=producto_id)
                    producto.cantidad += cantidad_cambio
                    producto.save()
                except productos.DoesNotExist:
                    continue  # Si el producto no existe, saltar al siguiente cambio

            return JsonResponse({"success": True})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})

    return JsonResponse({"success": False, "error": "Método no permitido"})

# -------------------------------------------------------------
def lista_ventas(request):
    ventas = Venta.objects.all()
    return render(request, 'registro.html', {'ventas': ventas})

# -------------------------------------------------------------
def detalle_venta(request, venta_id):
    venta = get_object_or_404(Venta, id=venta_id)
    if request.method == 'POST':
        try:
            with transaction.atomic():
                # Actualizar nombre_cliente si se proporciona
                nuevo_nombre_cliente = request.POST.get('nombre_cliente')
                if nuevo_nombre_cliente:
                    venta.nombre_cliente = nuevo_nombre_cliente 

                # Actualizar estado si se proporciona
                nuevo_estado = request.POST.get('estado')
                if nuevo_estado:
                    venta.estado = nuevo_estado

                # Actualizar fecha si se proporciona
                nueva_fecha = request.POST.get('fecha_venta')
                if nueva_fecha:
                    venta.fecha_venta = nueva_fecha

                # Actualizar detalles de productos
                detalles_actualizados = []
                total_nuevo = 0

                for producto in venta.detalles:
                    producto_id = str(producto['id'])
                    
                    # Obtener los nuevos valores del formulario
                    nueva_cantidad = int(request.POST.get(f'cantidad_{producto_id}', producto['cantidad']))
                    nuevo_precio = float(request.POST.get(f'precio_{producto_id}', producto['precio_unitario']))
                    nuevo_contenido = request.POST.get(f'contenido_{producto_id}', producto['contenido'])
                    
                    # Calcular nuevo subtotal
                    subtotal = nueva_cantidad * nuevo_precio
                    total_nuevo += subtotal

                    # Actualizar el detalle del producto
                    detalles_actualizados.append({
                        'id': producto['id'],
                        'nombre': producto['nombre'],
                        'contenido': nuevo_contenido,
                        'cantidad': nueva_cantidad,
                        'precio_unitario': nuevo_precio,
                        'subtotal': subtotal
                    })

                # Actualizar la venta con los nuevos detalles y total
                venta.detalles = detalles_actualizados
                venta.total = total_nuevo
                venta.save()

                return redirect('detalle_venta', venta_id=venta.id)
        except Exception as e:
            print(f"Error al actualizar la venta: {str(e)}")
            return render(request, 'detalle_venta.html', {
                'venta': venta,
                'error': f"Error al actualizar la venta: {str(e)}"
            })

    return render(request, 'detalle_venta.html', {'venta': venta})

# -------------------------------------------------------------
def generar_pdf_venta(request, venta_id):
    # Obtener la venta
    venta = get_object_or_404(Venta, id=venta_id)
    
    # Preparar el contexto para la plantilla
    context = {
        'venta': venta,
        'detalles': venta.detalles,  # Los detalles ya están en el formato correcto
    }
    
    # Renderizar el template HTML
    template = get_template('pdf_factura.html')
    html = template.render(context)
    
    # Crear el PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="venta_{venta_id}.pdf"'
    
    # Generar PDF
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('Error al generar el PDF', status=500)
    
    return response