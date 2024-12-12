from django.db import models
from tienda.models import productos
# Create your models here.


class Venta(models.Model):
    producto        = models.ForeignKey(productos, on_delete=models.CASCADE)
    cantidad        = models.PositiveIntegerField()
    precio_unitario = models.PositiveIntegerField()
    total_venta     = models.PositiveIntegerField()
    fecha           = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Venta de {self.producto.nombre} - {self.fecha}"

    class Meta:
        verbose_name = 'Venta'
        verbose_name_plural = 'Ventas'
        ordering = ['-fecha']

class RegistroVenta(models.Model):
    nombre  = models.CharField(max_length=100)
    valor   = models.PositiveIntegerField()
    fecha   = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} - {self.valor}"