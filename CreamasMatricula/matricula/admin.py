from django.contrib import admin
from models import Usuario, Grado,Seccion, Taller, Alumno, Matricula, Nivel, Semestre, Colegio, Clase

class ClaseAdmin(admin.ModelAdmin):
    list_display = ('grado', 'semestre', 'colegio', 'nivel')
    list_filter = ('colegio', 'semestre')

class TallerAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'semestre', 'colegio', 'estado')
    list_filter = ('semestre', 'colegio')

class AlumnoAdmin(admin.ModelAdmin):
    list_display = ('nombreCompleto', 'colegio', 'semestre')
    list_filter = ('semestre', 'colegio')

admin.site.register(Nivel)
admin.site.register(Semestre)
admin.site.register(Usuario)
admin.site.register(Grado)
admin.site.register(Seccion)
admin.site.register(Colegio)
admin.site.register(Clase, ClaseAdmin)
admin.site.register(Taller, TallerAdmin)
admin.site.register(Alumno, AlumnoAdmin)
admin.site.register(Matricula)
