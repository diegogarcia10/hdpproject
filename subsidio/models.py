from django.db import models
# Create your models here.
from django.contrib.auth.models import User


class TipoSubsidio(models.Model):
    nombre_tipo_subsidio = models.CharField(max_length=50)   
    def __str__(self):
        return '{}'.format(self.nombre_tipo_subsidio)


class Zona(models.Model):
    nombre_zona = models.CharField(max_length=50)
    def __str__(self):
        return '{}'.format(self.nombre_zona)
    
class Departamento(models.Model):
    codigo_zona = models.ForeignKey(Zona, on_delete=models.CASCADE, blank=False, null=False)
    nombre_departamento = models.CharField(max_length=50)   
    def __str__(self):
        return '{}'.format(self.nombre_departamento)
    
class Municipio (models.Model):
    codigo_departamento = models.ForeignKey(Departamento,on_delete=models.CASCADE, blank=False, null=False)
    nombre_municipio = models.CharField(max_length=50)        
    def __str__(self):
        return '{}'.format(self.nombre_municipio)

class Beneficiario (models.Model):
    codigo_municipio = models.ForeignKey(Municipio,  on_delete=models.PROTECT)
    codigo_usuario = models.ForeignKey(User, on_delete=models.PROTECT)
    DUI = models.CharField(max_length=9, blank=False, null=False, unique=True)
    NIT = models.CharField(max_length=20,blank=True, null=True, unique=True)        
    def __str__(self):
        return '{}'.format(self.codigo_usuario.first_name)

class BeneficiarioTipoSubsidio(models.Model):
    codigo_subsidio = models.ForeignKey(TipoSubsidio,  on_delete=models.PROTECT)
    codigo_beneficiario = models.ForeignKey(Beneficiario, on_delete=models.PROTECT)
    cantidad = models.DecimalField(max_digits=10, decimal_places=5)
    fecha = models.DateField(auto_now=False, auto_now_add=True)   
    def __str__(self):
        return '{}'.format(self.codigo_subsidio)
