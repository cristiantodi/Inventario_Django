from django.db import models
from tienda.models import productos

# Create your models here.
class MetodoPago(models.Model):
    nombre      = models.CharField(max_length=70)

    def __str__(self):
        return self.nombre
    
class CrearCreadito(models.Model):
    nombre      = models.CharField(max_length=100)
    documento   = models.PositiveIntegerField()
    producto    = models.ForeignKey(productos, on_delete=models.DO_NOTHING, blank=True)
    metodoPago  = models.ManyToManyField(MetodoPago, blank=True)
    registroPago= models.JSONField(default=list)
    
    def __str__(self):
        return self.nombre

    @property
    def num_abonos(self): # Calcula el número de abonos realizados
        return len(self.registroPago)

    @property
    def total_abonado(self): #Calcula el total de montos abonados
        return sum(pago.get('cantidad', 0) for pago in self.registroPago)