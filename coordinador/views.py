import pandas as pd
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Estudiante
from .forms import EstudianteForm
from django.http import HttpResponse
import openpyxl

# Create your views here.

def agregar_estudiante(request):
    if request.method == 'POST':
        form = EstudianteForm(request.POST)
        if form.is_valid():
            nombre = form.cleaned_data['nombre']
            email = form.cleaned_data['correo_electronico']
            rut = form.cleaned_data['rut']
            
            # Verificar si ya existe un usuario con el mismo username (RUT)
            if User.objects.filter(username=rut).exists():
                messages.error(request, "El RUT ya está registrado.")
                return render(request, 'coordinador/agregar_estudiante.html', {'form': form})

            # Crear el usuario usando el modelo User de Django
            usuario = User.objects.create_user(username=rut, email=email, first_name=nombre)
            usuario.set_password('password123')  # Configurar contraseña predeterminada
            usuario.save()

            grupo, creado = Group.objects.get_or_create(name='Estudiantes')
            usuario.groups.add(grupo)

            estudiante = Estudiante(
                usuario=usuario,
                rut=rut,
                domicilio=form.cleaned_data['domicilio'],
                carrera=form.cleaned_data['carrera']
            )
            estudiante.save()

            messages.success(request, "Estudiante agregado exitosamente.")
            return redirect('coordinador:listar_estudiantes')
    else:
        form = EstudianteForm()
    return render(request, 'coordinador/agregar_estudiante.html', {'form': form})

Group.objects.get_or_create(name='Estudiantes')

def carga_masiva_estudiantes(request):
    if request.method == 'POST':
        archivo = request.FILES.get('archivo')
        if not archivo:
            messages.error(request, "Por favor, selecciona un archivo.")
            return redirect('coordinador:carga_masiva_estudiantes')

        # Procesar el archivo Excel
        try:
            # Leer el archivo Excel
            df = pd.read_excel(archivo, engine='openpyxl')

            # Asegúrate de que el archivo tiene las columnas correctas
            columnas_esperadas = {'Nombre Completo', 'Correo Electrónico', 'RUT', 'Domicilio', 'Carrera'}
            if not columnas_esperadas.issubset(df.columns):
                messages.error(request, "El archivo no tiene las columnas requeridas.")
                return redirect('coordinador:carga_masiva_estudiantes')

            # Procesar cada fila del archivo
            for _, row in df.iterrows():
                nombre = row['Nombre Completo']
                email = row['Correo Electrónico']
                rut = row['RUT']
                domicilio = row['Domicilio']
                carrera = row['Carrera']

                # Verificar si ya existe un usuario con el mismo RUT
                if User.objects.filter(username=rut).exists():
                    messages.warning(request, f"El RUT {rut} ya está registrado y será omitido.")
                    continue

                # Crear el usuario en el sistema
                usuario = User.objects.create_user(username=rut, email=email, first_name=nombre)
                usuario.set_password('password123')
                usuario.save()

                grupo, creado = Group.objects.get_or_create(name='Estudiantes')
                usuario.groups.add(grupo)

                # Crear el estudiante asociado al usuario
                estudiante = Estudiante(
                    usuario=usuario,
                    rut=rut,
                    domicilio=domicilio,
                    carrera=carrera
                )
                estudiante.save()

            messages.success(request, "Carga masiva completada.")
            return redirect('coordinador:listar_estudiantes')

        except Exception as e:
            messages.error(request, f"Error al procesar el archivo: {e}")
            return redirect('coordinador:carga_masiva_estudiantes')

    return render(request, 'coordinador/carga_masiva_estudiantes.html')

def descargar_plantilla_estudiantes(request):
    # Define las columnas de la plantilla
    columnas = ['Nombre Completo', 'Correo Electrónico', 'RUT', 'Domicilio', 'Carrera']
    
    # Crear un DataFrame vacío con las columnas
    df = pd.DataFrame(columns=columnas)

    # Crear un archivo Excel en memoria
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=plantilla_estudiantes.xlsx'
    
    # Guardar el DataFrame como un archivo Excel en la respuesta
    df.to_excel(response, index=False, engine='openpyxl')
    
    return response
@login_required
def listar_estudiantes(request):
    estudiantes = Estudiante.objects.all()  # Obtiene todos los estudiantes
    return render(request, 'coordinador/listar_estudiantes.html', {'estudiantes': estudiantes})