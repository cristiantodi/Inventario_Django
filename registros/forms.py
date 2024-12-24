from django import forms

class FiltroMesAnioForm(forms.Form):
    YEAR_CHOICES = [(str(year), str(year)) for year in range(2000, 2031)]  # Años del 2000 al 2030
    MONTH_CHOICES = [
        ('1', 'Enero'),
        ('2', 'Febrero'),
        ('3', 'Marzo'),
        ('4', 'Abril'),
        ('5', 'Mayo'),
        ('6', 'Junio'),
        ('7', 'Julio'),
        ('8', 'Agosto'),
        ('9', 'Septiembre'),
        ('10', 'Octubre'),
        ('11', 'Noviembre'),
        ('12', 'Diciembre')
    ]

    mes = forms.ChoiceField(choices=MONTH_CHOICES, label='Mes')
    anio = forms.ChoiceField(choices=YEAR_CHOICES, label='Año')