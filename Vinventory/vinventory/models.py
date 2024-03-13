from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_delete

# Create your models here.

class Estante(models.Model):
    estante = models.CharField(max_length=50)
    def __str__(self) -> str:
        return self.estante

class Variedad(models.Model):
    variedad = models.CharField(max_length=50)
    def __str__(self) -> str:
        return self.variedad

class Origen(models.Model):
    origen = models.CharField(max_length=50)
    def __str__(self) -> str:
        return self.origen

class Bodega(models.Model):
    bodega = models.CharField(max_length=50)
    def __str__(self) -> str:
        return self.bodega

class Vino(models.Model):
    nombre = models.CharField(max_length=100)
    bodega = models.ForeignKey(Bodega, on_delete=models.CASCADE)
    variedad = models.ForeignKey(Variedad, on_delete=models.CASCADE)
    cosecha = models.PositiveSmallIntegerField()
    origen = models.ForeignKey(Origen, on_delete=models.CASCADE)
    cantidad = models.PositiveSmallIntegerField()
    codigo = models.BigIntegerField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    estante = models.ForeignKey(Estante, on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to="catalogo/", default='catalogo/default.png') #se van a guardar en media/catalogo
