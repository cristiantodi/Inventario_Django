
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .forms import AbonoForm
from .models import Abono

# Create your views here.


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

# def buscar_nombre(request):
#     documento = request.GET.get('documento', None)
#     if documento:
#         try:
#             abono = Abono.objects.get(documento=documento)
#             return JsonResponse({'nombre': abono.nombre}, status=200)
#         except Abono.DoesNotExist:
#             return JsonResponse({'error': 'No se encontró el documento'}, status=404)
#     return JsonResponse({'error': 'No se proporcionó el documento'}, status=400)

def get_nombre(request):
    documento = request.GET.get('documento', None)
    if documento:
        abono = Abono.objects.filter(documento=documento).first()
        if abono:
            return JsonResponse({'nombre': abono.nombre})
    return JsonResponse({'nombre': ''})
