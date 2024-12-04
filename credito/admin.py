from django.contrib import admin
from .models import CrearCreadito, MetodoPago

# Register your models here.

class MetodoPagoAdmin(admin.ModelAdmin):
    list_display = ["nombre"]

class CreditoAdmin(admin.ModelAdmin):
    list_display = ["id","nombre", "documento", "registroPago"]

admin.site.register(CrearCreadito, CreditoAdmin)
admin.site.register(MetodoPago, MetodoPagoAdmin)