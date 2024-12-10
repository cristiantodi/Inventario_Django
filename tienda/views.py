from django.shortcuts import render, get_object_or_404, redirect
from tienda.models import productos
from registros.models import RegistroVenta
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt

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
# @csrf_exempt
# def vender_productos(request):
#     if request.method == 'POST':
#         data = json.loads(request.body)
        
#         for id, producto in data.items():
#             prod = productos.objects.get(id=id)
#             prod.cantidad -= producto['cantidad']
#             if prod.cantidad < 0:
#                 return JsonResponse({'error': 'Stock insuficiente'}, status=400)
#             prod.save()
        
#         return JsonResponse({'status': 'success'})
#     return JsonResponse({'error': 'Método no permitido'}, status=405)
@csrf_exempt
def vender_productos(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        
        for id, producto in data.items():
            prod = productos.objects.get(id=id)
            cantidad_vendida = producto['cantidad']
            
            # Registrar venta
            RegistroVenta.objects.create(
                nombre=prod.nombre,
                valor=prod.precio * cantidad_vendida
            )

            prod.cantidad -= cantidad_vendida
            if prod.cantidad < 0:
                return JsonResponse({'error': 'Stock insuficiente'}, status=400)
            prod.save()
        
        return JsonResponse({'status': 'success'})
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