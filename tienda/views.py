from django.shortcuts import render
from tienda.models import productos
from django.http import JsonResponse
import json
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

