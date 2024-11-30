from django.contrib import admin
from .models import Abono, Metodo_pago

# Register your models here.

class MetodoPagoAdmin(admin.ModelAdmin):
    list_display = ["nombre_Pago"]

class AbonoAdmin(admin.ModelAdmin):
    list_display = ["id","nombre", "documento", "num_pagos", "mostrar_productos", "mostrar_metodo_pago", "num_pagos", "num_pagos_total"]

admin.site.register(Abono, AbonoAdmin)
admin.site.register(Metodo_pago, MetodoPagoAdmin)