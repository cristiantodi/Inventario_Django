from django import forms
from .models import Abono, Metodo_pago, productos

class AbonoForm(forms.ModelForm):
    producto = forms.ModelMultipleChoiceField(
        queryset=productos.objects.all(), 
        widget=forms.SelectMultiple(attrs={'class': 'form-select'}),
        required=False
    )
    metodo_pago = forms.ModelMultipleChoiceField(
        queryset=Metodo_pago.objects.all(), 
        widget=forms.SelectMultiple(attrs={'class': 'form-select'}),
        required=False
    )

    class Meta:
        model = Abono
        fields = ['nombre', 'documento', 'num_pagos', 'producto', 'num_pagos_total', 'metodo_pago']
        widgets = {
            # 'producto': forms.Select(attrs={'class': 'form-select'}),  # Lista desplegable para producto
            # 'metodo_pago': forms.SelectMultiple(attrs={'class': 'form-select'}),  # Lista desplegable para método de pago
        }
        