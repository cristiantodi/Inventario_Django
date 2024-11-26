from django import forms
from .models import Abono, Metodo_pago

# class AbonoForm(forms.ModelForm):
#     class Meta:
#         model = Abono
#         fields = ['nombre', 'documento', 'producto', 'num_pagos','num_pagos_total']

# class AbonoForm(forms.ModelForm):
#     metodo_pago = forms.ModelMultipleChoiceField(
#         queryset=Metodo_pago.objects.all(),
#         widget=forms.CheckboxSelectMultiple,
#         required=False,
#     )

#     class Meta:
#         model = Abono
#         fields = ['documento', 'nombre', 'num_pagos', 'num_pagos_total', 'metodo_pago']

class AbonoForm(forms.ModelForm):
    class Meta:
        model = Abono
        fields = ['nombre', 'documento', 'num_pagos', 'producto', 'num_pagos_total', 'metodo_pago']
        widgets = {
            'metodo_pago': forms.SelectMultiple(attrs={'class': 'form-select'}),
        }