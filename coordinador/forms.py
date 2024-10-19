from django import forms
from .models import Estudiante

class EstudianteForm(forms.ModelForm):
    nombre = forms.CharField(max_length=100, label="Nombre Completo")
    correo_electronico = forms.EmailField(label="Correo Electrónico")
    numero_telefono = forms.CharField(max_length=15, label="Número de Teléfono")
    rut = forms.CharField(max_length=20, label="RUT")
    domicilio = forms.CharField(max_length=255, label="Domicilio")
    carrera = forms.CharField(max_length=100, label="Carrera")
    
    class Meta:
        model = Estudiante
        fields = ['nombre', 'correo_electronico', 'numero_telefono', 'rut', 'domicilio', 'carrera']
    def clean_rut(self):
        rut = self.cleaned_data.get('rut')
        if Estudiante.objects.filter(rut=rut).exists():
            raise forms.ValidationError("El RUT ya está registrado.")
        return rut