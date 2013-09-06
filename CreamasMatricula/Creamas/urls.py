from django.conf.urls import patterns, include, url
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'Creamas.views.home', name='home'),
    # url(r'^Creamas/', include('Creamas.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # Debe de quitar el creamas/ para subirlo al apache de linux

	url(r'^admin/', include(admin.site.urls)),
	url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
	url(r'^login$', 'matricula.views.loginUsuario'),
	#url(r'^creamas/matricula$', 'matricula.views.listado_matricula'), deprecated
	url(r'^matricula-registrar$', 'matricula.views.registro_matricula'),
	url(r'^matricula-registrar/(\d+)$', 'matricula.views.modificacion_matricula'),
	url(r'^matricula-listar-alumnos$', 'matricula.views.listado_alumnos'),
	url(r'^matricula-registrar-alumno$', 'matricula.views.registro_alumno'),
	url(r'^matricula-seguimiento$', 'matricula.views.reporte_seguimiento'),
	url(r'^matricula-reporte$', 'matricula.views.reporte_matricula'),
	url(r'^logout$', 'matricula.views.logout_matricula'),

	url(r'^registrar_matricula$', 'matricula.views.guardar_matricula'),
	#Backend
	url(r'^listar_matricula', 'matricula.views.back_listar_matricula'),

	#Modificacion de matricula
	#url(r'^creamas/matricula-listar$', 'matricula.views.listado_matricula')
	url(r'^matricula-modificar-listar$', 'matricula.views.listado_matricula'),
	url(r'^matricula-modificar/(\d+)$', 'matricula.views.modificacion_matricula'),
	url(r'^matricula-eliminar/(\d+)$', 'matricula.views.eliminar_matricula'),
)
