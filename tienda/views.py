from django.shortcuts import render, get_object_or_404, redirect
from tienda.models import productos
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
@csrf_exempt
def vender_productos(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        
        for id, producto in data.items():
            prod = productos.objects.get(id=id)
            prod.cantidad -= producto['cantidad']
            if prod.cantidad < 0:
                return JsonResponse({'error': 'Stock insuficiente'}, status=400)
            prod.save()
        
        return JsonResponse({'status': 'success'})
    return JsonResponse({'error': 'Método no permitido'}, status=405)
# ----------------------------------------INVENTARIO------------------------------------------------------
def lista_productos(request):
    query = request.GET.get('query')
    productos_list = productos.objects.all()

    # Verifica si la consulta de búsqueda existe
    if query:
        try:
            # Si es un número, busca por ID
            producto_id = int(query)
            productos_list = productos_list.filter(id=producto_id)
        except ValueError:
            # Si no es un número, busca por nombre
            productos_list = productos_list.filter(nombre__icontains=query)

    # Manejo de incremento o decremento de la cantidad
    if request.method == 'POST':
        producto = get_object_or_404(productos, id=request.POST.get('producto_id'))
        accion = request.POST.get('accion')
        if accion == 'incrementar':
            producto.cantidad += 1
        elif accion == 'decrementar' and producto.cantidad > 0:
            producto.cantidad -= 1
        producto.save()
        return redirect('lista_productos')

    return render(request, 'inventario.html', {'productos': productos_list})
