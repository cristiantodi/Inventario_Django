from django import forms
from .models import Abono

class AbonoForm(forms.ModelForm):
    class Meta:
        model = Abono
        fields = ['nombre', 'documento','num_pagos','num_pagos_total']
