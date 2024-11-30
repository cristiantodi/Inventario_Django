from django.db import models

from tienda.models import productos

# Create your models here.

class Metodo_pago(models.Model):
    nombre_Pago      = models.CharField(max_length=70)

    def __str__(self):
        return self.nombre_Pago

class Abono(models.Model):
    nombre          = models.CharField(max_length=70)
    documento       = models.PositiveIntegerField()
    metodo_pago     = models.ManyToManyField(Metodo_pago, blank=True)
    producto        = models.ForeignKey(productos, on_delete=models.DO_NOTHING, blank=True)
    num_pagos       = models.PositiveSmallIntegerField( )
    num_pagos_total = models.PositiveSmallIntegerField()


    def mostrar_productos(self):
        # return ", ".join([str(prod) for prod in self.producto.all()])
        return str(self.producto) if self.producto else "Sin producto"
    
    def mostrar_metodo_pago(self):
        return ", ".join([str(met_pago) for met_pago in self.metodo_pago.all()])

    mostrar_productos.short_description = 'Productos'
    mostrar_metodo_pago.short_description = 'Metodo_Pago'
