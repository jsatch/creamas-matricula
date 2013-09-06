#!/usr/bin/env python
# -*- coding: utf-8 -*- 

from django.contrib.auth import authenticate, login, logout
from django.db import transaction
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.template.loader import get_template
from django.template import RequestContext
from django.conf import settings
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import logout_then_login
import json
import logging
from django.core.exceptions import ObjectDoesNotExist
from models import Matricula, Alumno, Clase, Semestre, Taller, Nivel
from forms import MatriculaForm, FiltroAlumnosForm, AlumnoForm, LoginForm
from models import ABIERTO, CERRADO, ACTIVO, INACTIVO, MATRICULADO, NOMATRICULADO

@csrf_exempt
def loginUsuario(request):
	if request.method == 'GET':
		loginForm = LoginForm()
		return render_to_response('login.html', {'form':loginForm}, context_instance=RequestContext(request))
	else:
		loginForm = LoginForm(request.POST)
		if loginForm.is_valid():
			username = loginForm.cleaned_data['username']
			password = loginForm.cleaned_data['password']
			colegio = loginForm.cleaned_data['colegio']

			user = authenticate(username=username, password=password)
			if user is not None:
				# the password verified for the user
				if user.is_active:
					print("User is valid, active and authenticated")
					login(request, user)

					request.session['colegio'] = colegio

					listaGrupos = user.groups.all()
					grupoStr = []
					for grupo in listaGrupos:
						grupoStr.append(grupo.name)


					if "administrador" in grupoStr:
						request.session['seguridad'] = "administrador"
					elif "digitador" in grupoStr:
						request.session['seguridad'] = "digitador"
					elif "visualizador" in grupoStr:
						request.session['seguridad'] = "visualizador"
						return redirect('/creamas/matricula-seguimiento')

					return redirect('/creamas/matricula-registrar')
				else:
					print("The password is valid, but the account has been disabled!")
					loginForm = LoginForm()
					mensaje ='El password es valido pero el usuario ha sido deshabilitado'
					return render_to_response('login.html', {'form':loginForm, 'mensaje': mensaje}, context_instance=RequestContext(request))
			else:
				# the authentication system was unable to verify the username and password
				print("The username and password were incorrect.")
				loginForm = LoginForm()
				mensaje ='El usuario y el password son incorrectos'
				return render_to_response('login.html', {'form':loginForm, 'mensaje': mensaje}, context_instance=RequestContext(request))
		else:
			return render_to_response('login.html', {'form':loginForm}, context_instance=RequestContext(request))

@login_required
def logout_matricula(request):
	return logout_then_login(request, login_url='/creamas/login')

# Cambio de modificar matricula
@login_required
@csrf_exempt
def listado_matricula(request):
	#listado_alumnos(request):
	if request.method == 'GET':
		filtroAlumnosForm = FiltroAlumnosForm()
		return render_to_response('matricula-listar.html', {'form':filtroAlumnosForm}, context_instance=RequestContext(request))
	else:
		listadoAlumnosMatriculados = []
		filtroAlumnosForm = FiltroAlumnosForm(request.POST)

		if filtroAlumnosForm.is_valid():
			grado = filtroAlumnosForm.cleaned_data['grado']
			nombre = filtroAlumnosForm.cleaned_data['nombre']
			colegio = request.session['colegio']

			#listadoAlumnosMatriculados = Matricula.objects.filter(alumno_nombreCompleto__icontains=nombre)

			if grado == None:
				listadoAlumnosMatriculados = Matricula.objects.filter(alumno__nombreCompleto__icontains=nombre).filter(alumno__colegio__exact=colegio)
			else:
				listadoAlumnosMatriculados = Matricula.objects.filter(alumno__grado__exact=grado).filter(alumno__nombreCompleto__icontains=nombre).filter(alumno__colegio__exact=colegio)
		else:
			print "Formulario no es valido"

		return render_to_response('matricula-listar.html', {'form':filtroAlumnosForm, 'listado_alumnos_matriculados': listadoAlumnosMatriculados}, context_instance=RequestContext(request))

@login_required
@csrf_exempt
def listado_alumnos(request):
	if request.method == 'GET':
		filtroAlumnosForm = FiltroAlumnosForm()
		return render_to_response('matricula-listar-alumnos.html', {'form':filtroAlumnosForm}, context_instance=RequestContext(request))
	else:
		listadoAlumnos = []
		filtroAlumnosForm = FiltroAlumnosForm(request.POST)

		if filtroAlumnosForm.is_valid():
			grado = filtroAlumnosForm.cleaned_data['grado']
			nombre = filtroAlumnosForm.cleaned_data['nombre']
			colegio = request.session['colegio']
			semestre = Semestre.objects.filter(estado__exact='A')[0]

			if grado == None:
				listadoAlumnos = Alumno.objects.filter(nombreCompleto__icontains=nombre).filter(colegio__exact=colegio).filter(semestre__exact=semestre)
			else:
				listadoAlumnos = Alumno.objects.filter(grado__exact=grado).filter(nombreCompleto__icontains=nombre).filter(colegio__exact=colegio).filter(semestre__exact=semestre)
			

		return render_to_response('matricula-listar-alumnos.html', {'form':filtroAlumnosForm, 'listado_alumnos': listadoAlumnos}, context_instance=RequestContext(request))

@login_required
@csrf_exempt
def registro_alumno(request):
	if request.method == 'GET':
		alumnoForm = AlumnoForm()
		return render_to_response('matricula-registrar-alumno.html', {'form':alumnoForm}, context_instance=RequestContext(request))
	else:
		alumnoForm = AlumnoForm(request.POST)
		if alumnoForm.is_valid():
			nombreCompleto = alumnoForm.cleaned_data['nombreCompleto']
			grado = alumnoForm.cleaned_data['grado']
			seccion = alumnoForm.cleaned_data['seccion']
			#nivel = alumnoForm.cleaned_data['nivel']
			colegio = request.session['colegio']
			telefono = alumnoForm.cleaned_data['telefono']
			tutor = alumnoForm.cleaned_data['tutor']
			semestre = alumnoForm.cleaned_data['semestre']
			fechaNacimiento = alumnoForm.cleaned_data['fechaNacimiento']

			alumnoBean = Alumno()
			alumnoBean.nombreCompleto = nombreCompleto
			alumnoBean.grado = grado
			alumnoBean.seccion = seccion
			alumnoBean.nivel = grado.nivel
			alumnoBean.colegio = colegio
			alumnoBean.telefono = telefono
			alumnoBean.tutor = tutor
			alumnoBean.semestre = semestre
			alumnoBean.fechaNacimiento = fechaNacimiento
			alumnoBean.estado = NOMATRICULADO

			alumnoBean.save()

			return render_to_response('matricula-registrar-alumno.html', {'alumno':alumnoBean}, context_instance=RequestContext(request))
		else:
			return render_to_response('matricula-registrar-alumno.html', {'form': alumnoForm}, context_instance=RequestContext(request))

@login_required
def registro_matricula(request):
	seguridad = request.session['seguridad']
	colegio = request.session['colegio']
	semestre = Semestre.objects.filter(estado__exact='A')[0]
	matriculaForm = MatriculaForm(colegio, semestre)

	return render_to_response('matricula-registrar.html', {'form':matriculaForm, 'seguridad':seguridad}, context_instance=RequestContext(request))

@login_required
def modificacion_matricula(request, idmatricula):
	if request.method == 'GET':
		matricula = Matricula.objects.get(id=idmatricula)

		matriculaForm = MatriculaForm(instance=matricula)

	return render_to_response('matricula-registrar.html', {'form':matriculaForm}, context_instance=RequestContext(request))

# Metodos del backend

@csrf_exempt
def guardar_matricula(request):
	if request.method == 'POST':
		colegio = request.session['colegio']
		matriculaForm = MatriculaForm(colegio,request.POST)
		if matriculaForm.is_valid():
			
			semestre = matriculaForm.cleaned_data['semestre']
			alumno = matriculaForm.cleaned_data['alumno']
			taller = matriculaForm.cleaned_data['taller']
			idAlumno = matriculaForm.cleaned_data['idAlumno']
			tutor = matriculaForm.cleaned_data['tutor']
			telefono = matriculaForm.cleaned_data['telefono']
			fechaNacimiento = matriculaForm.cleaned_data['fechaNacimiento']

			# Comprobamos que no se hayan cubierto las vacantes para taller ni para mate
			if taller.numeroVacantes <= taller.numeroInscritos:
				mensaje = "No hay cupos de taller disponibles"
				return render_to_response('matricula-registrar.html', {'form':matriculaForm, 'error':mensaje, 'seguridad':request.session['seguridad']}, context_instance=RequestContext(request)) 

			alumnoBean = Alumno.objects.get(id=idAlumno)
			clase = Clase.objects.filter(grado__exact=alumnoBean.grado).filter(colegio__exact=colegio)[0]

			if clase.numeroVacantes <= clase.numeroInscritos:
				mensaje = "No hay cupos de clase de matematicas disponibles"
				return render_to_response('matricula-registrar.html', {'form':matriculaForm, 'error':mensaje, 'seguridad':request.session['seguridad']}, context_instance=RequestContext(request)) 

			
			alumnoBean.tutor = tutor
			alumnoBean.telefono = telefono
			alumnoBean.fechaNacimiento = fechaNacimiento
			alumnoBean.estado = MATRICULADO
			alumnoBean.save()
			matricula = Matricula()
			matricula.semestre = semestre
			matricula.alumno = alumnoBean
			matricula.taller = taller

			matricula.save()
			
			#Debemos disminuir los disponibles para taller y para clase
			numInscritos = taller.numeroInscritos
			taller.numeroInscritos = numInscritos + 1
			print taller.numeroInscritos
			taller.save()

			numInscritos = clase.numeroInscritos
			clase.numeroInscritos = numInscritos + 1
			clase.save()

			
			matriculaForm = MatriculaForm(colegio)

			mensaje = "Matricula guardada exitosamente"
		else:
			
			#matriculaForm = MatriculaForm(colegio)
			mensaje = "Error procesando formulario, llene todos los campos"
			return render_to_response('matricula-registrar.html', {'form':matriculaForm, 'error':mensaje, 'seguridad':request.session['seguridad']}, context_instance=RequestContext(request))

	return render_to_response('matricula-registrar.html', {'form':matriculaForm, 'mensaje':mensaje, 'seguridad':request.session['seguridad']}, context_instance=RequestContext(request))

@csrf_exempt
def modificacion_matricula(request, idmatricula):
	colegio = request.session['colegio']
	matricula = Matricula.objects.get(pk=idmatricula)
	if request.method == 'GET':
		
		print matricula.semestre.nombre
		matriculaForm = MatriculaForm(colegio)
		#matriculaForm.taller.value = matricula.taller
		return render_to_response('matricula-modificar.html', {'matricula':matricula,'form':matriculaForm}, context_instance=RequestContext(request))
	else:
		#matriculaForm = MatriculaForm(colegio,request.POST)

		taller_id = request.POST['taller']
		taller_nuevo = Taller.objects.get(pk=taller_id)

		matricula = Matricula.objects.get(pk=idmatricula)
		taller_antiguo = matricula.taller

		#Disminuimos cuota a taller anterior

		if taller_nuevo.numeroInscritos <= taller_nuevo.numeroVacantes-1:
			print "Puede matricular porque " + str(taller_nuevo.numeroInscritos) + "<=" + str(taller_nuevo.numeroVacantes)
			#Podemos realizar la matricula
			#Aumentamos cuota a taller nuevo
			taller_nuevo.numeroInscritos = taller_nuevo.numeroInscritos + 1
			taller_antiguo.numeroInscritos = taller_antiguo.numeroInscritos - 1

			matricula.taller = taller_nuevo
			matricula.save()

			taller_nuevo.save()
			taller_antiguo.save()
			return HttpResponseRedirect("/creamas/matricula-modificar-listar")
		else:
			#No puede realizar matricula porque taller esta lleno
			return render_to_response('matricula-modificar.html', {'matricula':matricula,'form':matriculaForm}, context_instance=RequestContext(request))


		

	

@csrf_exempt
def eliminar_matricula(request, idmatricula):
	if request.method == 'GET':
		colegio = request.session['colegio']
		matricula = Matricula.objects.get(id=idmatricula)
		alumno = matricula.alumno
		
		# Se disminuiran los numero de inscritos del taller y de la clase a la que pertenecian
		taller = matricula.taller
		clase = Clase.objects.filter(grado__exact=alumno.grado).filter(colegio__exact=colegio)[0]
		taller.numeroInscritos = taller.numeroInscritos - 1
		clase.numeroInscritos = clase.numeroInscritos - 1

		# Cambiamos el estado del alumno a NOMATRICULADO
		alumno.estado = NOMATRICULADO

		matricula.delete()
		taller.save()
		clase.save()
		alumno.save()

	return HttpResponseRedirect("/creamas/matricula-modificar-listar")

@csrf_exempt
def back_listar_matricula(request): #ok
	if request.method == 'POST':
		#inputStr = request.body
		#jsInput = json.loads(inputStr)
		lista = []
		try:
			#id_evento = jsInput['id']
			lista_matriculas = Matricula.objects.all()
			for matricula in lista_matriculas:
				nombre = matricula.alumno.nombreCompleto
				dict_matricula = {'idmatricula':matricula.id, 'alumno':nombre, 'grado': matricula.alumno.grado.nombre, 'seccion': matricula.alumno.seccion.nombre, 'taller': matricula.taller.nombre, 'email': matricula.alumno.email}
				lista.append(dict_matricula)
			
			
		except ObjectDoesNotExist:
			return HttpResponse(json.dumps({'mensaje' : 'No hay registros'}), content_type="application/json")

		dict_output = {'mensaje' : '', 'lista_matriculas': lista}
		
		return HttpResponse(json.dumps(dict_output), content_type="application/json")

@login_required
def reporte_seguimiento(request):

	seguridad = request.session['seguridad']

	colegio = request.session['colegio']

	semestre = Semestre.objects.filter(estado__exact=ACTIVO)[0]

	niveles = Nivel.objects.all()

	talleres_total = {}
	for nivel in niveles:
		talleres = Taller.objects.filter(nivel__exact=nivel).filter(semestre__exact=semestre).filter(colegio__exact=colegio)
		talleres_total[str(nivel.nombre)] = talleres

	clases_total = {}
	for nivel in niveles:
		clases = Clase.objects.filter(nivel__exact=nivel).filter(semestre__exact=semestre).filter(colegio__exact=colegio)
		clases_total[str(nivel.nombre)] = clases

	return render_to_response('matricula-seguimiento.html', {'talleres':talleres_total, 'clases':clases_total, 'seguridad':seguridad}, context_instance=RequestContext(request))

def reporte_matricula(request):

	seguridad = request.session['seguridad']

	#colegio = request.session['colegio']

	semestre = Semestre.objects.filter(estado__exact=ACTIVO)[0]

	lista_matricula = Matricula.objects.all();

	return render_to_response('matricula-reporte.html', {'lista_matricula':lista_matricula, 'seguridad':seguridad}, context_instance=RequestContext(request))

def migrar_alumnos_semestre(request):
	from matricula.models import Semestre, Alumno, NOMATRICULADO
	semestre = Semestre.objects.filter(estado__exact='A')[0]
	nombre_semestre_anterior = "2013-I"

	semestre = Semestre.objects.filter(estado__exact='A')[0]
	semestre_ant = Semestre.objects.filter(nombre__exact=nombre_semestre_anterior)[0]

	listado_alumnos = Alumno.objects.filter(semestre__exact=semestre_ant)
	for alumno in listado_alumnos:
		alumno.pk = None
		alumno.semestre = semestre
		alumno.estado = NOMATRICULADO
		alumno.save()
