from django.shortcuts import render

from .models import Abono
# Create your views here.

def abonos(request):
    clientes =  Abono.objects.all()
    return render(request,"abono.html", {"clientes": clientes})