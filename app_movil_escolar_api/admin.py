from django.contrib import admin

from django.utils.html import format_html
from app_movil_escolar_api.models import *

#implementar la logica para los ALUMNOS y maestros
@admin.register(Administradores)
class AdministradoresAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "clave_admin", "telefono", "rfc", "edad", "ocupacion")
    search_fields = ("user__username", "user__email", "user__first_name", "user__last_name")

@admin.register(Alumnos)
class AlumnosAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "clave_alumno", "telefono", "fecha_nacimiento", "rfc", "curp", "edad", "ocupacion")
    search_fields = ("user__username", "user__email", "user__first_name", "user__last_name")

@admin.register(Maestros)
class MaestrosAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "clave_maestro", "fecha_nacimiento", "telefono", "rfc", "materias_json", "cubiculo", "area_investigacion")
    search_fields = ("user__username", "user__email", "user__first_name", "user__last_name")

@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):
    list_display = ("id", "descripcion", "fecha", "hora_inicio", "hora_fin", "publico_objetivo", "lugar", "nombre", "nombre_responsable", "tipo", "numero_participantes", "programa_educativo")
    search_fields = ("nombre", "nombre_responsable", "tipo")