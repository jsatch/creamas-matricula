from django.contrib import admin
from models import Usuario, Grado,Seccion, Taller, Alumno, Matricula, Nivel, Semestre, Colegio, Clase

class ClaseAdmin(admin.ModelAdmin):
    list_display = ('grado', 'semestre', 'colegio', 'nivel')

admin.site.register(Nivel)
admin.site.register(Semestre)
admin.site.register(Usuario)
admin.site.register(Grado)
admin.site.register(Seccion)
admin.site.register(Colegio)
admin.site.register(Clase, ClaseAdmin)
admin.site.register(Taller)
admin.site.register(Alumno)
admin.site.register(Matricula)
