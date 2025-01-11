from django.shortcuts import render, get_object_or_404, redirect
from .models import productos, Venta
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
import logging

from django.template.loader import render_to_string
# from weasyprint import HTML


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

                    prod.cantidad -= cantidad_vendida
                    prod.save()

                    # RegistroVenta.objects.create(
                    #     nombre=prod.nombre,
                    #     valor=prod.precio * cantidad_vendida
                    # )
                    logger.info(f'Venta registrada para producto {prod.nombre}')
            
            return JsonResponse({'status': 'success'})
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

def vender_productos(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            total = sum(float(item['precio']) * int(item['cantidad']) 
                       for item in data.values())
            
            with transaction.atomic():
                # Crear el registro de venta
                venta = Venta.objects.create(
                    total=total,
                    detalles=data
                )
                
                # Actualizar el inventario
                for id, producto in data.items():
                    try:
                        prod = productos.objects.get(id=id)
                        cantidad_vendida = producto.get('cantidad', 0)
                        if prod.cantidad < cantidad_vendida:
                            raise Exception(f'Stock insuficiente para {prod.nombre}')
                        prod.cantidad -= cantidad_vendida
                        prod.save()
                    except productos.DoesNotExist:
                        raise Exception(f'Producto con ID {id} no encontrado')
                
            return JsonResponse({'status': 'success', 'venta_id': venta.id})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Método no permitido'}, status=405)

def lista_ventas(request):
    ventas = Venta.objects.all()
    return render(request, 'registro.html', {'ventas': ventas})

def detalle_venta(request, venta_id):
    venta = get_object_or_404(Venta, id=venta_id)
    if request.method == 'POST':
        try:
            with transaction.atomic():
                # Actualizar estado si se proporciona
                nuevo_estado = request.POST.get('estado')
                if nuevo_estado:
                    venta.estado = nuevo_estado

                # Actualizar fecha si se proporciona
                nueva_fecha = request.POST.get('fecha_venta')
                if nueva_fecha:
                    venta.fecha_venta = nueva_fecha

                # Actualizar detalles de productos
                detalles_actualizados = {}
                total_nuevo = 0

                for key, value in request.POST.items():
                    if key.startswith('cantidad_') or key.startswith('precio_'):
                        producto_id = key.split('_')[1]
                        if producto_id not in detalles_actualizados:
                            detalles_actualizados[producto_id] = venta.detalles.get(producto_id, {}).copy()
                        
                        if key.startswith('cantidad_'):
                            detalles_actualizados[producto_id]['cantidad'] = int(value)
                        elif key.startswith('precio_'):
                            detalles_actualizados[producto_id]['precio'] = float(value)

                # Calcular nuevo total y actualizar detalles
                for producto_id, detalles in detalles_actualizados.items():
                    if 'cantidad' in detalles and 'precio' in detalles:
                        subtotal = detalles['cantidad'] * detalles['precio']
                        total_nuevo += subtotal

                venta.total = total_nuevo
                venta.detalles = detalles_actualizados
                venta.save()

                return redirect('detalle_venta', venta_id=venta.id)
        except Exception as e:
            # Aquí podrías agregar un mensaje de error
            print(f"Error al actualizar la venta: {str(e)}")
            return render(request, 'detalle_venta.html', {
                'venta': venta,
                'error': f"Error al actualizar la venta: {str(e)}"
            })

    return render(request, 'detalle_venta.html', {'venta': venta})

# def generar_pdf_venta(request, venta_id):
#     venta = get_object_or_404(Venta, id=venta_id)
    
#     # Renderizar el template HTML
#     html_string = render_to_string('pdf_venta.html', {'venta': venta})
    
#     # Crear el PDF
#     html = HTML(string=html_string)
#     result = html.write_pdf()
    
#     # Generar la respuesta HTTP
#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = f'attachment; filename="venta_{venta_id}.pdf"'
#     response.write(result)
    
#     return response