from django.shortcuts import render, get_object_or_404, redirect
from tienda.models import productos
from django.http import JsonResponse
import json
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

@csrf_exempt
def tienda(request):    
    products=productos.objects.all()
    
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            products = data.get('products', [])
            
            for item in products:
                product_id = item['id']
                cantidad = item['cantidad']

                # Obtener el producto y actualizar la cantidad en la base de datos
                product = productos.objects.get(id=product_id)
                if product.cantidad >= cantidad:
                    product.cantidad -= cantidad
                    product.save()
                else:
                    return JsonResponse({'success': False, 'error': 'No hay suficiente inventario para uno de los productos'})

            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return render(request, "tienda.html", {"products":products})

# ----------------------------------------------------------------------------------------------

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

# def lista_productos(request):
#     producto_id = request.GET.get('producto_id')
#     productos_list = productos.objects.all()

#     # Si se ingresa un ID, obtener el producto específico
#     if producto_id:
#         productos_list = productos_list.filter(id=producto_id)

#     # Manejo de incremento o decremento de la cantidad
#     if request.method == 'POST':
#         producto = get_object_or_404(productos, id=request.POST.get('producto_id'))
#         accion = request.POST.get('accion')
#         if accion == 'incrementar':
#             producto.cantidad += 1
#         elif accion == 'decrementar' and producto.cantidad > 0:
#             producto.cantidad -= 1
#         producto.save()
#         return redirect('lista_productos')

#     return render(request, 'inventario.html', {'productos': productos_list})