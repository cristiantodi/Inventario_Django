from django.db import models

# Create your models here.

class categoria(models.Model):
    nombre          = models.CharField(max_length=50)
    imagenCategoria = models.ImageField(upload_to='Categoria_Tienda', null=True, blank=True)
    created         = models.DateTimeField(auto_now_add=True)
    updated         = models.DateTimeField(auto_now_add=True)
    # created = models.DateTimeField(auto_now_add=True)
    # updated = models.DateTimeField(auto_now=True) 
    # MIRAR, QUE CUANDO SE REALICE UN CAMBIO GUARDE QUE USUARIO LO REALIZO

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
    # created = models.DateTimeField(auto_now_add=True)
    # updated = models.DateTimeField(auto_now=True) 
    # MIRAR, QUE CUANDO SE REALICE UN CAMBIO GUARDE QUE USUARIO LO REALIZO
    class Meta:
        verbose_name='producto'
        verbose_name_plural='productos'

    def __str__(self):
        return self.nombre