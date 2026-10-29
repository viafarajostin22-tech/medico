from django.db import models

class PuestoSalud(models.Model):
    PUESTOS_CHOICES = [
        ('Rodeo', 'Rodeo'),
        ('Rivera', 'Rivera'),
        ('Petecuy', 'Petecuy'),
    ]
    nombre = models.CharField(max_length=50, choices=PUESTOS_CHOICES, unique=True)

    def __str__(self):
        return self.nombre


class RegistroUsuario(models.Model):
    puesto = models.ForeignKey(PuestoSalud, on_delete=models.CASCADE, related_name='usuarios')
    nombre_usuario = models.CharField(max_length=100, verbose_name="Nombre del Usuario")
    documento = models.CharField(max_length=20, verbose_name="Documento")
    
    # Pruebas disponibles y sus tarifas
    microbiologia = models.BooleanField(default=False, verbose_name="Microbiología ($15.000)")
    bacteriologia = models.BooleanField(default=False, verbose_name="Bacteriología ($25.000)")
    quimica = models.BooleanField(default=False, verbose_name="Química ($35.000)")
    
    total_a_pagar = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def calcular_total(self):
        total = 0
        if self.microbiologia:
            total += 15000
        if self.bacteriologia:
            total += 25000
        if self.quimica:
            total += 35000
        return total

    def save(self, *args, **kwargs):
        self.total_a_pagar = self.calcular_total()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nombre_usuario} - {self.puesto.nombre}"