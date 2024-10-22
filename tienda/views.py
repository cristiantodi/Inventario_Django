from django.shortcuts import render
from tienda.models import productos

# Create your views here.

def tienda(request):    
    products=productos.objects.all()
    return render(request, "tienda.html", {"products":products})