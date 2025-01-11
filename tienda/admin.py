from django.contrib import admin
from .models import productos, categoria, productoImagen, Venta

class productoImagenInline(admin.TabularInline):  # Nombre corregido
    model = productoImagen
    extra = 3  # Cantidad de campos adicionales para subir imágenes

@admin.register(productos)
class ProductoAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "nombre",
        "imagen",
        "contenido",
        "precio",
        "mostrar_categorias",
        "cantidad",
        "disponibilidad",
        "created",
        "updated",
    )
    inlines = [productoImagenInline]  # Nombre corregido aquí

    def mostrar_categorias(self, obj):
        return ", ".join([category.nombre for category in obj.categoria.all()])

    mostrar_categorias.short_description = 'Categoria'
    search_fields = ("nombre", "contenido", "precio", "created", "updated")
    list_filter = ("created",)
    date_hierarchy = "created"

@admin.register(categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("id", "imagenCategoria", "created", "updated")
    search_fields = ("nombre", "updated")
    list_filter = ("created", "updated")
    date_hierarchy = "created"

@admin.register(Venta)
class VentaAdmin(admin.ModelAdmin):
    list_display = ("id", "fecha_venta", "detalles", "total")
