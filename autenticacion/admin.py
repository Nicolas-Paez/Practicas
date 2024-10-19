from django.contrib import admin
from .models import Profile

# Registrar el modelo Profile en el panel de administración
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'rut')
    search_fields = ('user__username', 'rut')