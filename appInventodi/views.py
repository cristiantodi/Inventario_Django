from django.shortcuts import render
from django.contrib.auth.models import Group
from tienda.models import productos, categoria
from django.contrib.auth import get_user_model

User=get_user_model()
# Create your views here.

def contactanos(request):
    return render(request,"contacto.html")

def home(request):
    products = productos.objects.prefetch_related('imagenes').all()
    categorias = categoria.objects.all()
    grupos = Group.objects.all()  # Obtener todos los grupos
    return render(request, "home.html", {'grupos': grupos, 'products': products, 'categorias': categorias})

def lista_productos(request):
    query = request.GET.get('buscar')
    if query:
        products = productos.objects.filter(nombre__icontains=query)
    return render(request, 'home.html', {'products': products})

