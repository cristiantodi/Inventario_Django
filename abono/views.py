
from django.shortcuts import render, redirect
from .forms import AbonoForm
from .models import Abono

# Create your views here.


def abonos(request):
    clientes =  Abono.objects.all()
    print("----------------------------------------------------------------------------------------")
    return render(request,"abono.html", {"clientes": clientes})


def crearAbono(request):
    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    form = AbonoForm()  # Crea una instancia del formulario
    if request.method == 'POST':
        form = AbonoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('Abonos')  # Redirige para evitar reenviar el formulario
    return render(request, 'crear.html', {'form': form})

