from django.contrib import admin
from .models import productos, categoria

# Register your models here.

class categoriaAdmin(admin.ModelAdmin):
    list_display=(
        "id",
        "imagenCategoria",
        "created",
        "updated",
    )
    # readonly_fields=("created","updated")
    search_fields=("nombre","updated") #campo de busqueda
    list_filter=("created","updated") #Filtrar
    date_hierarchy="created" #visualizacion del filtro

class productoAdmin(admin.ModelAdmin):
    list_display=(
        "id",
        "nombre",
        "imagen",
        # "categoria",
        "contenido",
        "precio",        
        "mostrar_categorias",        
        "cantidad",
        "disponibilidad",
        "created",
        "updated",
    )
    def mostrar_categorias(self, obj):
        return ", ".join([category.nombre for category in obj.categoria.all()])

    mostrar_categorias.short_description = 'Categoria'
    # readonly_fields=("created","updated")
    search_fields=("nombre", "contenido", "precio","created", "updated") #campo de busqueda
    list_filter=("created",) #Filtrar
    date_hierarchy="created" #visualizacion del filtro

admin.site.register(productos, productoAdmin)
admin.site.register(categoria, categoriaAdmin)