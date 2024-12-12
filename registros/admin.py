from django.contrib import admin

from .models import RegistroVenta, Venta

# Register your models here.

@admin.register(Venta)
class VentaAdmin(admin.ModelAdmin):
    list_display = ('producto', 'cantidad', 'precio_unitario', 'total_venta', 'fecha')
    list_filter = ('fecha', 'producto')
    search_fields = ('producto__nombre',)

class registroAdmin(admin.ModelAdmin):
    list_display=(
        "id",
        "nombre",
        "valor",
        "fecha",
    )

admin.site.register(RegistroVenta, registroAdmin)