from django.shortcuts import render, get_object_or_404, redirect
from tienda.models import productos
from registros.models import RegistroVenta
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
import logging

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

                    RegistroVenta.objects.create(
                        nombre=prod.nombre,
                        valor=prod.precio * cantidad_vendida
                    )
                    logger.info(f'Venta registrada para producto {prod.nombre}')
            
            return JsonResponse({'status': 'success'})
        except Exception as e:
            logger.error(f'Error inesperado: {str(e)}')
            return JsonResponse({'error': f'Ocurrió un error inesperado: {str(e)}'}, status=500)
    return JsonResponse({'error': 'Método no permitido'}, status=405)

# @csrf_exempt
# def vender_productos(request):
#     if request.method == 'POST':
#         try:
#             data = json.loads(request.body)
            
#             # Abrir una transacción para garantizar consistencia
#             with transaction.atomic():
#                 for id, producto in data.items():
#                     # Validar que el producto exista
#                     try:
#                         prod = productos.objects.get(id=id)
#                     except productos.DoesNotExist:
#                         return JsonResponse({'error': f'Producto con ID {id} no encontrado'}, status=404)
                    
#                     # Validar que la cantidad solicitada sea válida
#                     cantidad_vendida = producto.get('cantidad', 0)
#                     if not isinstance(cantidad_vendida, int) or cantidad_vendida <= 0:
#                         return JsonResponse({'error': f'Cantidad inválida para el producto con ID {id}'}, status=400)

#                     # Verificar stock disponible
#                     if prod.cantidad < cantidad_vendida:
#                         return JsonResponse({'error': f'Stock insuficiente para el producto {prod.nombre}'}, status=400)

#                     # Registrar venta
#                     RegistroVenta.objects.create(
#                         nombre=prod.nombre,
#                         valor=prod.precio * cantidad_vendida
#                     )

#                     # Actualizar stock
#                     prod.cantidad -= cantidad_vendida
#                     prod.save()
            
#             return JsonResponse({'status': 'success'})
#         except json.JSONDecodeError:
#             return JsonResponse({'error': 'Datos JSON inválidos'}, status=400)
#         except Exception as e:
#             # Log para depuración
#             return JsonResponse({'error': f'Ocurrió un error inesperado: {str(e)}'}, status=500)
#     return JsonResponse({'error': 'Método no permitido'}, status=405)


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