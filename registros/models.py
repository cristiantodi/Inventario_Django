from django.db import models

# Create your models here.

class RegistroVenta(models.Model):
    nombre  = models.CharField(max_length=100)
    valor   = models.PositiveIntegerField()
    fecha   = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} - {self.valor}"