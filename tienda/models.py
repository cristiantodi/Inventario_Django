from django.db import models

# Create your models here.

class categoria(models.Model):
    nombre          = models.CharField(max_length=50)
    imagenCategoria = models.ImageField(upload_to='Categoria_Tienda', null=True, blank=True)
    created         = models.DateTimeField(auto_now_add=True)
    updated         = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name='categoria'
        verbose_name_plural='categorias'

    def __str__(self):
        return self.nombre

class productos(models.Model):
    nombre          = models.CharField(max_length=50)
    imagen          = models.ImageField(upload_to='tienda', null=True, blank=True)
    categoria       = models.ManyToManyField(categoria, null=True, blank=True)
    contenido       = models.CharField(max_length=1000)    
    precio          = models.PositiveIntegerField()
    cantidad        = models.PositiveSmallIntegerField()
    disponibilidad  = models.BooleanField(default=True)
    created         = models.DateTimeField(auto_now_add=True)
    updated         = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name='producto'
        verbose_name_plural='productos'

class productoImagen(models.Model):
    producto    = models.ForeignKey(productos, on_delete=models.CASCADE, related_name='imagenes')
    imagen      = models.ImageField(upload_to='tienda/productos')

    def __str__(self):
        return f"Imagen de {self.producto.nombre}"

class Venta(models.Model):
    fecha_venta = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    detalles = models.JSONField()  # Almacenará los productos vendidos en formato JSON
    estado = models.CharField(max_length=20, default='completada')
    
    class Meta:
        verbose_name = 'venta'
        verbose_name_plural = 'ventas'
        ordering = ['-fecha_venta']  # Ordenar por fecha más reciente

    def __str__(self):
        return f"Venta #{self.id} - {self.fecha_venta.strftime('%Y-%m-%d %H:%M')}"
