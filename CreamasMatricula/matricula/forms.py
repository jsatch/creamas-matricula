#!/usr/bin/env python
# -*- coding: utf-8 -*- 

from django import forms
from django.db.models import F
from models import Matricula, Alumno, Taller, Nivel, Grado, Semestre, Colegio
from models import ABIERTO, CERRADO, ACTIVO, INACTIVO
from django.contrib.admin.widgets import AdminDateWidget 

class MatriculaForm(forms.Form):
	semestre = forms.ModelChoiceField(label='Semestre', queryset=Semestre.objects.filter(estado__exact=ACTIVO),empty_label=None)
	idAlumno = forms.CharField(widget=forms.HiddenInput)
	alumno = forms.CharField(label='Alumno', widget=forms.TextInput(attrs={'readonly':'readonly'}))
	taller = forms.ModelChoiceField(label='Taller', queryset=Taller.objects.filter(estado__exact=ABIERTO).filter(numeroVacantes__gt=F('numeroInscritos')),empty_label="----Seleccionar----")

	tutor = forms.CharField(label='Tutor', required=False)
	telefono = forms.CharField(label='Teléfono', required=False)
	telefonoEmergencia = forms.CharField(label='Telefono Emergencia', required=False)
	fechaNacimiento = forms.DateField(label='Fecha Nacimiento', widget=AdminDateWidget,required=False)
	email = forms.EmailField(label='Email', required=False)

	def __init__(self, colegio, *args, **kwargs):
		super(MatriculaForm, self).__init__(*args, **kwargs)
		self.fields['taller'] = forms.ModelChoiceField(label='Taller', queryset=Taller.objects.filter(estado__exact=ABIERTO).filter(colegio__exact=colegio).filter(numeroVacantes__gt=F('numeroInscritos')),empty_label="----Seleccionar----")

	#def __init__(self, colegio):
	#	self.colegio = colegio

class FiltroAlumnosForm(forms.Form):
	#nivel = forms.ModelChoiceField(label='Nivel', queryset=Nivel.objects.all(),empty_label="----Seleccionar----", required=True)
	grado = forms.ModelChoiceField(label='Grado', queryset=Grado.objects.filter(estado__exact=ACTIVO),empty_label="----Seleccionar----", required=True)
	nombre = forms.CharField(label='Nombre Completo', required=False, max_length=100)

class AlumnoForm(forms.ModelForm):
	semestre = forms.ModelChoiceField(label='Semestre', queryset=Semestre.objects.filter(estado__exact=ACTIVO),empty_label=None)
	class Meta:
		model = Alumno
		exclude = ('colegio','email', 'telefonoEmergencia', 'estado','nivel')

class LoginForm(forms.Form):
	username = forms.CharField(label='Usuario')
	password = forms.CharField(label='Password', widget=forms.PasswordInput)
	colegio = forms.ModelChoiceField(label='Colegio', queryset=Colegio.objects.filter(estado__exact=ACTIVO),empty_label="----Seleccionar----", required=True)
