from django.db import models

from tienda.models import productos

# Create your models here.

class Metodo_pago(models.Model):
    nombre_Pago      = models.CharField(max_length=70)

    def __str__(self):
        return self.nombre_Pago

class Abono(models.Model):
    nombre      = models.CharField(max_length=70)
    documento   = models.PositiveIntegerField()
    metodo_pago = models.ManyToManyField(Metodo_pago, blank=True)
    producto    = models.ManyToManyField(productos, blank=True)
    num_pagos   = models.PositiveSmallIntegerField()
    num_pagos_total   = models.PositiveSmallIntegerField()

    def mostrar_productos(self):
        return ", ".join([str(prod) for prod in self.producto.all()])

    mostrar_productos.short_description = 'Productos'
