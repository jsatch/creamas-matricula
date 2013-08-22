#!/usr/bin/env python
# -*- coding: utf-8 -*- 

from django.db import models

ACTIVO = 'A'
INACTIVO = 'I'
ABIERTO = 'B'
CERRADO = 'C'
MATRICULADO = 'M'
NOMATRICULADO = 'N'
ESTADO_CHOICES = (
    (ACTIVO, 'Activo'),
    (INACTIVO, 'Inactivo'),
)
TALLER_ESTADO_CHOICES = (
	(ABIERTO, 'Abierto'),
    (CERRADO, 'Cerrado'),
)
ALUMNO_ESTADO_CHOICES = (
	(MATRICULADO, 'Matriculado'),
    (NOMATRICULADO, 'No Matriculado'),
)

class Nivel(models.Model):
	nombre = models.CharField(max_length=50)
	def __unicode__(self):
		return self.nombre

class Semestre(models.Model):
	nombre = models.CharField(max_length=20)
	fechaInicio = models.DateField(blank=True, null=True)
	fechaFin = models.DateField(blank=True, null=True)
	estado = models.CharField(max_length=1, choices=ESTADO_CHOICES)
	def __unicode__(self):
		return self.nombre

class Usuario(models.Model):
	username = models.CharField(max_length=20)
	password = models.CharField(max_length=20)
	isAdmin = models.BooleanField(verbose_name="Es administrador?")
	def __unicode__(self):
		return self.username

class Colegio(models.Model):
	nombre = models.CharField(max_length=100)
	descripcion = models.TextField(max_length=300, blank=True, null=True)
	direccion = models.CharField(max_length=100, blank=True, null=True)
	telefonos = models.CharField(max_length=100, blank=True, null=True)
	director = models.CharField(max_length=100, blank=True, null=True)
	numeroInscritos = models.IntegerField(max_length=4, blank=True, null=True)
	estado = models.CharField(max_length=1, choices=ESTADO_CHOICES)
	def __unicode__(self):
		return self.nombre

class Grado(models.Model):
	nombre = models.CharField(max_length=50)
	nivel = models.ForeignKey(Nivel, verbose_name="Nivel")
	estado = models.CharField(max_length=1, choices=ESTADO_CHOICES)
	def __unicode__(self):
		return self.nombre

class Seccion(models.Model):
	nombre = models.CharField(max_length=20)
	estado = models.CharField(max_length=1, choices=ESTADO_CHOICES)
	def __unicode__(self):
		return self.nombre

class Clase(models.Model):
	grado = models.ForeignKey(Grado, verbose_name="Grado")
	nivel = models.ForeignKey(Nivel, verbose_name="Nivel")
	semestre = models.ForeignKey(Semestre, verbose_name="Semestre")
	colegio = models.ForeignKey(Colegio, verbose_name="Colegio")
	numeroCreandos = models.IntegerField(max_length=4, blank=True, null=True)
	numeroVacantes = models.IntegerField(max_length=4, blank=True, null=True)
	numeroInscritos = models.IntegerField(max_length=4, blank=True, null=True)
	estado = models.CharField(max_length=1, choices=TALLER_ESTADO_CHOICES)
	def __unicode__(self):
		return self.grado.nombre

class Taller(models.Model):
	nombre = models.CharField(max_length=50)
	descripcion = models.TextField(max_length=200, blank=True, null=True)
	semestre = models.ForeignKey(Semestre, verbose_name="Semestre")
	nivel = models.ForeignKey(Nivel, verbose_name="Nivel")
	colegio = models.ForeignKey(Colegio, verbose_name="Colegio")
	numeroCreandos = models.IntegerField(max_length=4, blank=True, null=True)
	numeroVacantes = models.IntegerField(max_length=4)
	numeroInscritos = models.IntegerField(max_length=4)
	estado = models.CharField(max_length=1, choices=TALLER_ESTADO_CHOICES)
	secciones = models.ManyToManyField(Seccion)
	def __unicode__(self):
		return self.nombre

class Alumno(models.Model):
	nombreCompleto = models.CharField(max_length=200, verbose_name="Nombre Completo")
	semestre = models.ForeignKey(Semestre, verbose_name="Semestre")
	grado = models.ForeignKey(Grado, verbose_name="Grado")
	seccion = models.ForeignKey(Seccion, verbose_name="Sección")
	nivel = models.ForeignKey(Nivel, verbose_name="Nivel")
	colegio = models.ForeignKey(Colegio, verbose_name="Colegio")
	telefono = models.CharField(max_length=15, verbose_name="Teléfono")
	tutor = models.CharField(max_length=100) # Debe ser tutor (no nombrePadre)
	telefonoEmergencia = models.CharField(max_length=15, blank=True, null=True)
	fechaNacimiento = models.DateField()
	email = models.EmailField(blank=True, null=True)
	fechaRegistro = models.DateField(auto_now_add=True)
	fechaActualizacion = models.DateField(auto_now=True)
	estado = models.CharField(max_length=1, choices=ALUMNO_ESTADO_CHOICES)
	def __unicode__(self):
		return self.nombreCompleto

class Matricula(models.Model):
	semestre = models.ForeignKey(Semestre, verbose_name="Semestre")
	alumno = models.ForeignKey(Alumno)
	taller = models.ForeignKey(Taller)
	fechaRegistro = models.DateField(auto_now_add=True)
	fechaActualizacion = models.DateField(auto_now=True)
	def __unicode__(self):
		return self.alumno.nombreCompleto + " - " + self.semestre.nombre
