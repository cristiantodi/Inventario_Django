from django import forms
from .models import CrearCreadito, MetodoPago
from tienda.models import productos

class CreditoForm(forms.ModelForm):
    metodo_pago = forms.ModelMultipleChoiceField(
        queryset    =MetodoPago.objects.all(), 
        widget      =forms.SelectMultiple(attrs={'class': 'form.metodo_pago'}),
        required    =True,
    )

    class Meta:
        model = CrearCreadito
        fields = [ 'documento', 'nombre', 'producto']
        widgets = {
            'producto': forms.Select(attrs={'class': 'form-select'}),  # Lista desplegable para producto
        }
        