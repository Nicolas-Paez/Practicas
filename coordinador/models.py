from django.db import models
from django.contrib.auth.models import User

# Modelo Coordinador
class Coordinador(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return f'Coordinador: {self.usuario.username}'

# Modelo Estudiante
class Estudiante(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    rut = models.CharField(max_length=20, unique=True)
    domicilio = models.CharField(max_length=255)
    carrera = models.CharField(max_length=100)

    def __str__(self):
        return f'Estudiante: {self.usuario.username}'

# Modelo Práctica
class Practica(models.Model):
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE)
    estado = models.CharField(max_length=50)
    fecha_inscripcion = models.DateField()

    def __str__(self):
        return f'Práctica {self.pk} - {self.estado}'

# Modelo Ficha de Inscripción
class FichaInscripcion(models.Model):
    practica = models.ForeignKey(Practica, on_delete=models.CASCADE)
    empresa = models.CharField(max_length=255)
    supervisor = models.CharField(max_length=255)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()

    def __str__(self):
        return f'Ficha Inscripción - Práctica {self.practica.pk}'

# Modelo Autoevaluación
class Autoevaluacion(models.Model):
    practica = models.ForeignKey(Practica, on_delete=models.CASCADE)
    nota = models.DecimalField(max_digits=3, decimal_places=1)
    observaciones = models.TextField()

    def __str__(self):
        return f'Autoevaluación - Práctica {self.practica.pk}'

# Modelo Informe Confidencial
class InformeConfidencial(models.Model):
    practica = models.ForeignKey(Practica, on_delete=models.CASCADE)
    rubrica = models.ForeignKey('Rubrica', on_delete=models.CASCADE)
    comentario = models.TextField()

    def __str__(self):
        return f'Informe Confidencial - Práctica {self.practica.pk}'

# Modelo Rubrica
class Rubrica(models.Model):
    tipo_informe = models.CharField(max_length=100)
    criterio1 = models.CharField(max_length=100)
    criterio2 = models.CharField(max_length=100)
    ponderacion_criterio1 = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f'Rubrica: {self.tipo_informe}'

# Modelo Informe de Avances
class InformeAvances(models.Model):
    practica = models.ForeignKey(Practica, on_delete=models.CASCADE)
    rubrica = models.ForeignKey(Rubrica, on_delete=models.CASCADE)
    nota_avance = models.DecimalField(max_digits=3, decimal_places=1)
    retroalimentacion = models.TextField()

    def __str__(self):
        return f'Informe Avances - Práctica {self.practica.pk}'

# Modelo Informe Final
class InformeFinal(models.Model):
    practica = models.ForeignKey(Practica, on_delete=models.CASCADE)
    rubrica = models.ForeignKey(Rubrica, on_delete=models.CASCADE)
    nota = models.DecimalField(max_digits=3, decimal_places=1)
    retroalimentacion = models.TextField()

    def __str__(self):
        return f'Informe Final - Práctica {self.practica.pk}'
