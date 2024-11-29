
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .forms import AbonoForm
from .models import Abono, Metodo_pago

# Create your views here. 

def metodoPago(request):
    metodo_Pago = Metodo_pago.objects.all()
    return render(request, 'tienda.html', {'metodo_Pago': metodo_Pago})


def abonos(request):
    query = request.GET.get('documento', None)
    if query:
        clientes = Abono.objects.filter(documento=query)
    else:
        clientes = Abono.objects.all()
    return render(request, "abono.html", {"clientes": clientes})


def crearAbono(request):
    form = AbonoForm()  # Crea una instancia del formulario
    if request.method == 'POST':
        form = AbonoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('Abonos')  # Redirige para evitar reenviar el formulario
    return render(request, 'crear.html', {'form': form})

def get_nombre(request):
    documento = request.GET.get('documento', None)
    if documento:
        abono = Abono.objects.filter(documento=documento).first()
        if abono:
            return JsonResponse({'nombre': abono.nombre})
    return JsonResponse({'nombre': ''})
