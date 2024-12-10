
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.timezone import now
from django.http import JsonResponse
from .forms import CreditoForm
from .models import CrearCreadito, MetodoPago

# Create your views here. 

def metodoPago(request):
    Metodo_Pago = MetodoPago.objects.all()
    return render(request, 'tienda.html', {'Metodo_Pago': Metodo_Pago})


def creditos(request):
    credito = CrearCreadito.objects.all()
    return render(request, "credito.html", {"clientes" : credito})

# ----------------------------------------

def crear_credito(request):
    if request.method == "POST":
        form = CreditoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('Creditos')  # Redirigir a la página principal después de guardar
    else:
        form = CreditoForm()
    return render(request, 'crear.html', {'form': form})

#------------------------------------------

def abonar(request, credito_id):
    credito = get_object_or_404(CrearCreadito, id=credito_id)
    if request.method == "POST":
        metodo_pago_id = request.POST.get('metodo_pago')
        cantidad = int(request.POST.get('cantidad'))
        
        registro_actual = credito.registroPago or [] # Actualizar el JSONField de registroPago
        nuevo_registro = {
            'cantidad': cantidad,
            'metodo_pago': MetodoPago.objects.get(id=metodo_pago_id).nombre,
            "fecha": now().strftime("%Y-%m-%d %H:%M:%S")
        }
        registro_actual.append(nuevo_registro)
        credito.registroPago = registro_actual
        credito.save()
        return redirect('Creditos')  # Redirigir a la lista de créditos

    metodos_pago = MetodoPago.objects.all()
    return render(request, 'pago.html', {
        'credito': credito,
        'metodos_pago': metodos_pago
    })

# def abonar(request, credito_id):
#     credito = get_object_or_404(CrearCreadito, id=credito_id)
#     if request.method == "POST":
#         metodo_pago_id = request.POST.get('metodo_pago')
#         cantidad = float(request.POST.get('cantidad'))

#         # Crear un nuevo registro de abono con la fecha actual
#         nuevo_abono = {
#             "cantidad": int(cantidad),
#             "metodo_pago": MetodoPago.objects.get(id=metodo_pago_id).nombre,
#             "fecha": now().strftime("%Y-%m-%d %H:%M:%S")  # Formato de fecha y hora
#         }

#         # Agregar el nuevo abono al campo registroPago
#         credito.registroPago.append(nuevo_abono)
#         credito.save()

#         return redirect('Creditos')

#     return render(request, 'pago.html', {'credito': credito})
# ----------------------------------------

def ver_registros(request, credito_id):
    credito = get_object_or_404(CrearCreadito, id=credito_id)
    registros = credito.registroPago  # Obtiene el JSONField
    return render(request, 'ver.html', {'credito': credito, 'registros': registros})