from django.contrib import admin

from .models import RegistroVenta

# Register your models here.

class registroAdmin(admin.ModelAdmin):
    list_display=(
        "id",
        "nombre",
        "valor",
        "fecha",
    )

admin.site.register(RegistroVenta, registroAdmin)