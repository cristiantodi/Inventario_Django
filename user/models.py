from django.contrib.auth.models import AbstractUser
from django.db import models
# from appMyWeb import models

# Create your models here.

class Cargo(models.Model):
    nombre  = models.CharField(blank=True , default="N/A" , null=True, max_length=50)
    
    def __str__(self):
        return self.nombre

class User(AbstractUser):
    cargo   = models.ManyToManyField(Cargo)
    local   = models.CharField(blank=True , default="N/A" , null=True, max_length=50)