from django.contrib import admin
from .models import (Coordinador, Estudiante, Practica, FichaInscripcion, Autoevaluacion, 
                     InformeConfidencial, Rubrica, InformeAvances, InformeFinal)

admin.site.register(Coordinador)
admin.site.register(Estudiante)
admin.site.register(Practica)
admin.site.register(FichaInscripcion)
admin.site.register(Autoevaluacion)
admin.site.register(InformeConfidencial)
admin.site.register(Rubrica)
admin.site.register(InformeAvances)
admin.site.register(InformeFinal)
